"""
app.py - Flask application entry point for AI Student Assistant.
CSS and JS are served from _css.py and _js.py Python modules so they are
always present regardless of Vercel static-file deployment behaviour.
"""
import os
from flask import Flask, request, jsonify, render_template, Response

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import database as db
import ai_service as ai

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

@app.before_request
def _init():
    db.init_db()

# ── Static asset routes (CSS + JS served from Python modules) ─────────────
@app.route("/static/style.css")
def serve_css():
    from _css import CONTENT
    return Response(CONTENT, mimetype="text/css")

@app.route("/static/script.js")
def serve_js():
    from _js import CONTENT
    return Response(CONTENT, mimetype="application/javascript")

# ── Page ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", ai_configured=ai.is_configured())

# ── Conversations ─────────────────────────────────────────────────────────
@app.route("/api/conversations", methods=["GET"])
def list_conversations():
    try:
        return jsonify({"conversations": db.list_conversations()})
    except Exception:
        return jsonify({"error": "Could not load conversations."}), 500

@app.route("/api/conversations", methods=["POST"])
def create_conversation():
    data  = request.get_json(silent=True) or {}
    title = (data.get("title") or "New Conversation").strip()[:255]
    try:
        return jsonify(db.create_conversation(title)), 201
    except Exception:
        return jsonify({"error": "Could not create conversation."}), 500

@app.route("/api/conversations/<int:conv_id>", methods=["GET"])
def get_conversation(conv_id):
    try:
        conv = db.get_conversation(conv_id)
        if not conv:
            return jsonify({"error": "Conversation not found."}), 404
        return jsonify({"conversation": conv, "messages": db.get_messages(conv_id)})
    except Exception:
        return jsonify({"error": "Could not load conversation."}), 500

@app.route("/api/conversations/<int:conv_id>", methods=["DELETE"])
def delete_conversation(conv_id):
    try:
        if not db.delete_conversation(conv_id):
            return jsonify({"error": "Conversation not found."}), 404
        return jsonify({"message": "Conversation deleted successfully."})
    except Exception:
        return jsonify({"error": "Could not delete conversation."}), 500

# ── Chat ──────────────────────────────────────────────────────────────────
@app.route("/api/chat", methods=["POST"])
def chat():
    data     = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()
    conv_id  = data.get("conversation_id")

    if not question:
        return jsonify({"error": "Please enter a question."}), 400
    if len(question) > 10000:
        return jsonify({"error": "Question is too long (max 10,000 characters)."}), 400
    if not ai.is_configured():
        return jsonify({"error": "ai_not_configured",
                        "message": "Set AI_API_KEY in Vercel environment variables."}), 503
    try:
        if conv_id:
            conv = db.get_conversation(conv_id)
            if not conv:
                return jsonify({"error": "Conversation not found."}), 404
        else:
            title   = question[:60] + ("…" if len(question) > 60 else "")
            conv    = db.create_conversation(title)
            conv_id = conv["id"]

        history     = db.get_messages(conv_id)
        ai_messages = [{"role": m["role"], "content": m["content"]} for m in history]
        ai_messages.append({"role": "user", "content": question})
        answer = ai.get_ai_response(ai_messages)
        db.add_message(conv_id, "user",      question)
        db.add_message(conv_id, "assistant", answer)
        db.update_conversation_time(conv_id)
        return jsonify({"answer": answer, "conversation_id": conv_id,
                        "conversation": db.get_conversation(conv_id)})
    except ai.AIServiceNotConfigured as e:
        return jsonify({"error": "ai_not_configured", "message": str(e)}), 503
    except ai.AIServiceError as e:
        return jsonify({"error": "ai_error", "message": str(e)}), 502
    except Exception as e:
        app.logger.error("Error in /api/chat: %s", e)
        return jsonify({"error": "An unexpected error occurred."}), 500

# ── Search ────────────────────────────────────────────────────────────────
@app.route("/api/search", methods=["GET"])
def search():
    query = (request.args.get("q") or "").strip()
    if not query:
        return jsonify({"conversations": [], "query": ""})
    if len(query) > 500:
        return jsonify({"error": "Search query too long."}), 400
    try:
        return jsonify({"conversations": db.search_conversations(query), "query": query})
    except Exception:
        return jsonify({"error": "Search failed."}), 500

# ── Status / Debug ────────────────────────────────────────────────────────
@app.route("/api/status", methods=["GET"])
def status():
    return jsonify({"status": "ok", "ai_configured": ai.is_configured(),
                    "ai_model": os.environ.get("AI_MODEL", "gpt-4o-mini")})

@app.route("/api/debug/ai", methods=["GET"])
def debug_ai():
    key      = os.environ.get("AI_API_KEY", "")
    base_url = os.environ.get("AI_API_BASE_URL", "https://api.openai.com/v1")
    model    = os.environ.get("AI_MODEL", "gpt-4o-mini")
    info = {"key_present": bool(key),
            "key_prefix":  (key[:6] + "...") if key else "NOT SET",
            "base_url": base_url, "model": model,
            "test_result": None, "error": None}
    if key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=key, base_url=base_url)
            resp   = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Reply with exactly: OK"}],
                max_tokens=5)
            info["test_result"] = resp.choices[0].message.content.strip()
        except Exception as e:
            info["error"] = type(e).__name__ + ": " + str(e)[:300]
    return jsonify(info)

if __name__ == "__main__":
    db.init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
