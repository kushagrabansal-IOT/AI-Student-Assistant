"""
app.py
Flask application entry point for AI Student Assistant.
Loads environment variables, initialises the database,
and registers all API routes.
"""

import os
from flask import Flask, request, jsonify, render_template, abort

# Load .env file if python-dotenv is available (local dev)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # Not required — env vars may be set by the host/CI/Codespaces

import database as db
import ai_service as ai

# ── Application factory ───────────────────────────────────────────────────

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


@app.before_request
def _init():
    """Ensure the database and tables exist before the first request."""
    db.init_db()


# ═════════════════════════════════════════════════════════════════════════
# PAGE ROUTES
# ═════════════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    """Serve the main single-page application."""
    return render_template("index.html", ai_configured=ai.is_configured())


# ═════════════════════════════════════════════════════════════════════════
# API — CONVERSATIONS
# ═════════════════════════════════════════════════════════════════════════

@app.route("/api/conversations", methods=["GET"])
def list_conversations():
    """GET /api/conversations — return all conversations, newest first."""
    try:
        conversations = db.list_conversations()
        return jsonify({"conversations": conversations})
    except Exception as e:
        return jsonify({"error": "Could not load conversations."}), 500


@app.route("/api/conversations", methods=["POST"])
def create_conversation():
    """POST /api/conversations — create a new conversation."""
    data  = request.get_json(silent=True) or {}
    title = (data.get("title") or "New Conversation").strip()[:255]

    try:
        conv = db.create_conversation(title)
        return jsonify(conv), 201
    except Exception as e:
        return jsonify({"error": "Could not create conversation."}), 500


@app.route("/api/conversations/<int:conv_id>", methods=["GET"])
def get_conversation(conv_id: int):
    """GET /api/conversations/<id> — return a conversation and its messages."""
    try:
        conv = db.get_conversation(conv_id)
        if not conv:
            return jsonify({"error": "Conversation not found."}), 404

        messages = db.get_messages(conv_id)
        return jsonify({"conversation": conv, "messages": messages})
    except Exception as e:
        return jsonify({"error": "Could not load conversation."}), 500


@app.route("/api/conversations/<int:conv_id>", methods=["DELETE"])
def delete_conversation(conv_id: int):
    """DELETE /api/conversations/<id> — delete conversation and messages."""
    try:
        deleted = db.delete_conversation(conv_id)
        if not deleted:
            return jsonify({"error": "Conversation not found."}), 404
        return jsonify({"message": "Conversation deleted successfully."})
    except Exception as e:
        return jsonify({"error": "Could not delete conversation."}), 500


# ═════════════════════════════════════════════════════════════════════════
# API — CHAT
# ═════════════════════════════════════════════════════════════════════════

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    POST /api/chat
    Body: { "question": str, "conversation_id": int | null }

    1. Validate input.
    2. Create conversation if none provided.
    3. Load history for context.
    4. Send to AI.
    5. Save question + answer to database.
    6. Return answer + conversation_id.
    """
    data     = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()
    conv_id  = data.get("conversation_id")

    # ── Input validation ─────────────────────────────────────
    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    if len(question) > 10000:
        return jsonify({"error": "Question is too long (max 10,000 characters)."}), 400

    # ── Check AI is configured ───────────────────────────────
    if not ai.is_configured():
        return jsonify({
            "error":   "ai_not_configured",
            "message": (
                "The AI service is not configured. "
                "Please set the AI_API_KEY environment variable. "
                "See the README or .env.example for instructions."
            )
        }), 503

    try:
        # ── Get or create conversation ───────────────────────
        if conv_id:
            conv = db.get_conversation(conv_id)
            if not conv:
                return jsonify({"error": "Conversation not found."}), 404
        else:
            # Auto-generate title from first 60 chars of question
            title = question[:60] + ("…" if len(question) > 60 else "")
            conv  = db.create_conversation(title)
            conv_id = conv["id"]

        # ── Load conversation history for context ────────────
        history = db.get_messages(conv_id)
        ai_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in history
        ]
        ai_messages.append({"role": "user", "content": question})

        # ── Call the AI ──────────────────────────────────────
        answer = ai.get_ai_response(ai_messages)

        # ── Save to database ─────────────────────────────────
        db.add_message(conv_id, "user",      question)
        db.add_message(conv_id, "assistant", answer)
        db.update_conversation_time(conv_id)

        return jsonify({
            "answer":          answer,
            "conversation_id": conv_id,
            "conversation":    db.get_conversation(conv_id),
        })

    except ai.AIServiceNotConfigured as e:
        return jsonify({
            "error":   "ai_not_configured",
            "message": str(e),
        }), 503

    except ai.AIServiceError as e:
        return jsonify({
            "error":   "ai_error",
            "message": str(e),
        }), 502

    except Exception as e:
        app.logger.error("Unexpected error in /api/chat: %s", e)
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500


# ═════════════════════════════════════════════════════════════════════════
# API — SEARCH
# ═════════════════════════════════════════════════════════════════════════

@app.route("/api/search", methods=["GET"])
def search():
    """GET /api/search?q=<query> — search conversations and messages."""
    query = (request.args.get("q") or "").strip()

    if not query:
        return jsonify({"conversations": [], "query": ""})

    if len(query) > 500:
        return jsonify({"error": "Search query too long."}), 400

    try:
        results = db.search_conversations(query)
        return jsonify({"conversations": results, "query": query})
    except Exception as e:
        return jsonify({"error": "Search failed. Please try again."}), 500


# ═════════════════════════════════════════════════════════════════════════
# API — STATUS
# ═════════════════════════════════════════════════════════════════════════

@app.route("/api/status", methods=["GET"])
def status():
    """GET /api/status — returns application and AI config status."""
    return jsonify({
        "status":         "ok",
        "ai_configured":  ai.is_configured(),
        "ai_model":       os.environ.get("AI_MODEL", "gpt-4o-mini"),
        "ai_base_url":    os.environ.get("AI_API_BASE_URL", "https://api.openai.com/v1"),
    })


# ═════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    db.init_db()
    port  = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"\n🎓 AI Student Assistant")
    print(f"   Running at: http://localhost:{port}")
    print(f"   AI API:     {'✅ Configured' if ai.is_configured() else '⚠️  Not configured (set AI_API_KEY)'}")
    print(f"   Model:      {os.environ.get('AI_MODEL', 'gpt-4o-mini')}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
