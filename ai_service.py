"""
ai_service.py
AI integration layer for AI Student Assistant.
Uses an OpenAI-compatible API so it works with OpenAI, Azure OpenAI,
local models (Ollama), or any compatible provider.

API key is NEVER hard-coded — always read from environment variables.
If no key is configured, a clear user-facing error is returned.
"""

import os
from typing import Generator

# ── Configuration (read from environment) ────────────────────────────────

AI_API_KEY      = os.environ.get("AI_API_KEY", "")
AI_API_BASE_URL = os.environ.get("AI_API_BASE_URL", "https://api.openai.com/v1")
AI_MODEL        = os.environ.get("AI_MODEL", "gpt-4o-mini")

# System prompt — makes the AI behave as an educational tutor
SYSTEM_PROMPT = """You are an AI Student Assistant — a helpful, patient, and encouraging educational tutor.

Your job is to help students learn and understand academic concepts.

Guidelines:
- Explain concepts clearly using simple language appropriate for the student's apparent level.
- Always give concrete examples to illustrate abstract ideas.
- Break complex topics into smaller, digestible steps.
- Encourage curiosity and a growth mindset.
- When a student seems confused, rephrase your explanation from a different angle.
- If you are unsure about something, say so honestly rather than guessing.
- Format your answers clearly:
  • Use numbered lists for steps or sequences.
  • Use bullet points for related items.
  • Use code blocks for any programming examples.
  • Use headings to organise long answers.
- End answers with a brief follow-up question or suggestion to deepen understanding when appropriate.
- Be supportive and never make students feel bad for not knowing something.
- Avoid giving unexplained answers — always teach the "why", not just the "what".

You help with all academic subjects: mathematics, science, computer science,
history, literature, languages, and more."""


class AIServiceError(Exception):
    """Raised when the AI service cannot complete a request."""
    pass


class AIServiceNotConfigured(AIServiceError):
    """Raised when no API key has been set."""
    pass


def is_configured() -> bool:
    """Return True if an API key is present in the environment."""
    return bool(AI_API_KEY and AI_API_KEY.strip())


def get_ai_response(messages: list[dict]) -> str:
    """
    Send a conversation history to the AI and return the assistant's reply.

    Parameters
    ----------
    messages : list of dicts with 'role' and 'content' keys.
               Roles must be 'user' or 'assistant'.

    Returns
    -------
    str — the AI-generated response text.

    Raises
    ------
    AIServiceNotConfigured — if AI_API_KEY is not set.
    AIServiceError         — if the API call fails for any reason.
    """
    if not is_configured():
        raise AIServiceNotConfigured(
            "AI_API_KEY is not configured. "
            "Please set the AI_API_KEY environment variable. "
            "See .env.example for instructions."
        )

    # Build the full message list with system prompt
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    try:
        from openai import OpenAI, APIError, AuthenticationError, RateLimitError

        client = OpenAI(
            api_key=AI_API_KEY,
            base_url=AI_API_BASE_URL,
        )

        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=full_messages,
            max_tokens=2048,
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except ImportError:
        raise AIServiceError(
            "The 'openai' Python package is not installed. "
            "Run: pip install openai"
        )
    except AuthenticationError:
        raise AIServiceError(
            "Invalid AI_API_KEY. Please check that your API key is correct."
        )
    except RateLimitError:
        raise AIServiceError(
            "AI API rate limit reached. Please wait a moment and try again."
        )
    except APIError as e:
        raise AIServiceError(f"AI API error: {str(e)}")
    except Exception as e:
        raise AIServiceError(f"Unexpected error communicating with AI: {str(e)}")


def get_config_info() -> dict:
    """Return safe (non-secret) configuration info for debugging."""
    return {
        "configured":   is_configured(),
        "base_url":     AI_API_BASE_URL,
        "model":        AI_MODEL,
        "key_preview":  (AI_API_KEY[:6] + "…") if is_configured() else "NOT SET",
    }
