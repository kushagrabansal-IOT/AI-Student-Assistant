"""
database.py
Database layer for AI Student Assistant.
Uses SQLite by default — modular design allows replacing with PostgreSQL/Oracle later.
All queries use parameterized statements to prevent SQL injection.
"""

import sqlite3
import os
from datetime import datetime

# Database path — stored in /database/ folder
# Vercel has a read-only filesystem; /tmp is the only writable directory.
# Locally, store alongside the project in database/assistant.db.
if os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV"):
    DB_PATH = "/tmp/assistant.db"
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), "database", "assistant.db")


def get_connection():
    """Return a database connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # rows accessible as dicts
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """
    Create tables if they do not exist.
    Called automatically when the Flask app starts.
    """
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS conversations (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                title      TEXT    NOT NULL,
                created_at TEXT    NOT NULL DEFAULT (datetime('now')),
                updated_at TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS messages (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role            TEXT    NOT NULL CHECK(role IN ('user', 'assistant')),
                content         TEXT    NOT NULL,
                created_at      TEXT    NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_messages_conv
                ON messages(conversation_id);

            CREATE INDEX IF NOT EXISTS idx_conversations_updated
                ON conversations(updated_at DESC);
        """)


# ── Conversation Operations ──────────────────────────────────────────────

def create_conversation(title: str) -> dict:
    """Create a new conversation and return it."""
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO conversations (title, created_at, updated_at) VALUES (?, ?, ?)",
            (title, now, now)
        )
        row = conn.execute(
            "SELECT * FROM conversations WHERE id = ?", (cur.lastrowid,)
        ).fetchone()
        return dict(row) if row else None


def get_conversation(conv_id: int) -> dict | None:
    """Return a single conversation by ID, or None."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM conversations WHERE id = ?", (conv_id,)
        ).fetchone()
        return dict(row) if row else None


def list_conversations() -> list[dict]:
    """Return all conversations, newest first."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM conversations ORDER BY updated_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]


def update_conversation_time(conv_id: int) -> None:
    """Bump updated_at whenever a new message is added."""
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute(
            "UPDATE conversations SET updated_at = ? WHERE id = ?",
            (now, conv_id)
        )


def delete_conversation(conv_id: int) -> bool:
    """
    Delete a conversation and all its messages (CASCADE).
    Returns True if a row was deleted, False if ID not found.
    """
    with get_connection() as conn:
        cur = conn.execute(
            "DELETE FROM conversations WHERE id = ?", (conv_id,)
        )
        return cur.rowcount > 0


# ── Message Operations ───────────────────────────────────────────────────

def add_message(conv_id: int, role: str, content: str) -> dict:
    """Insert a message and return it."""
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO messages (conversation_id, role, content, created_at)
               VALUES (?, ?, ?, ?)""",
            (conv_id, role, content, now)
        )
        # Query within the same connection so the row is visible before commit
        row = conn.execute(
            "SELECT * FROM messages WHERE id = ?", (cur.lastrowid,)
        ).fetchone()
        return dict(row) if row else {
            "id": cur.lastrowid,
            "conversation_id": conv_id,
            "role": role,
            "content": content,
            "created_at": now,
        }


def get_messages(conv_id: int) -> list[dict]:
    """Return all messages for a conversation in chronological order."""
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT * FROM messages
               WHERE conversation_id = ?
               ORDER BY created_at ASC""",
            (conv_id,)
        ).fetchall()
        return [dict(r) for r in rows]


# ── Search ────────────────────────────────────────────────────────────────

def search_conversations(query: str) -> list[dict]:
    """
    Full-text search across conversation titles and message content.
    Returns matching conversations with a snippet of the matched message.
    Uses LIKE with parameterized queries — safe against SQL injection.
    """
    pattern = f"%{query}%"
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT DISTINCT c.id, c.title, c.created_at, c.updated_at
               FROM conversations c
               LEFT JOIN messages m ON m.conversation_id = c.id
               WHERE c.title LIKE ?
                  OR m.content LIKE ?
               ORDER BY c.updated_at DESC""",
            (pattern, pattern)
        ).fetchall()
        return [dict(r) for r in rows]
