# 🎓 AI Student Assistant

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/kushagrabansal-IOT/AI-Student-Assistant)

## 🌐 Live Demo

**Deployed on Vercel — open from your phone:**

🔗 **[ai-student-assistant-kushagrabansal94-3596.vercel.app](https://ai-student-assistant-kushagrabansal94-3596.vercel.app)**

> ⚠️ AI responses require `AI_API_KEY` to be configured in Vercel environment variables.
> The app loads, chat history, search, and delete all work without a key.
> To enable AI: go to [Vercel Dashboard → ai-student-assistant → Settings → Environment Variables](https://vercel.com/kushagrabansal94-3596/ai-student-assistant/settings/environment-variables) and add `AI_API_KEY`.

---


> **Your AI-powered learning companion** — a web application that lets students ask questions, get clear AI-generated explanations, and review their learning history.

---

## Overview

AI Student Assistant is a Flask web application that connects students to an AI tutor. Ask any question — maths, science, history, coding — and receive a clear, educational explanation. Every conversation is saved so you can review and search your learning history at any time.

---

## Features

| Feature | Description |
|---|---|
| 💬 AI Chat | Ask questions and receive educational AI responses |
| 📚 Conversation History | All chats saved and accessible in the sidebar |
| 🔍 Search | Search across all previous conversations and messages |
| 🗑️ Delete | Remove individual conversations with confirmation |
| ➕ New Chat | Start fresh conversations at any time |
| 📱 Responsive | Works on desktop, tablet, and mobile |
| ⚙️ Configurable AI | Works with OpenAI, Azure OpenAI, or any compatible provider |
| 🔒 Secure | API keys never stored in code or database |

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.10+, Flask |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Database | SQLite (via Python `sqlite3`) |
| AI | OpenAI-compatible REST API (`openai` Python package) |
| Config | Environment variables via `python-dotenv` |

---

## Project Structure

```
AI-Student-Assistant/
│
├── app.py              # Flask routes and API endpoints
├── ai_service.py       # AI API integration (OpenAI-compatible)
├── database.py         # SQLite database operations
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── .env.example        # Environment variable template
├── .gitignore          # Files excluded from git
│
├── templates/
│   └── index.html      # Single-page application HTML
│
├── static/
│   ├── style.css       # Application stylesheet
│   └── script.js       # Frontend JavaScript
│
├── database/           # SQLite database file stored here (git-ignored)
│   └── .gitkeep
│
└── screenshots/        # Add screenshots here
    └── .gitkeep
```

---

## Requirements

- Python 3.10 or higher
- An API key from an OpenAI-compatible AI provider (e.g. [OpenAI](https://platform.openai.com))
- Internet connection (to reach the AI API)

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/AI-Student-Assistant.git
cd AI-Student-Assistant
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows (Command Prompt):**
  ```bat
  venv\Scriptsctivate.bat
  ```
- **Windows (PowerShell):**
  ```powershell
  venv\Scripts\Activate.ps1
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

### 1. Create your `.env` file

```bash
cp .env.example .env
```

### 2. Edit `.env` and add your API key

```env
AI_API_KEY=sk-your-real-api-key-here
AI_API_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
```

> ⚠️ **Never commit your `.env` file.** It is listed in `.gitignore` to prevent accidental exposure of your API key.

---

## Run the Application

```bash
python app.py
```

Open your browser at: **http://localhost:5000**

---

## GitHub Codespaces

1. Open the repository in GitHub Codespaces.
2. The terminal opens automatically in the project directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your API key as a Codespace secret, **or** create `.env`:
   ```bash
   cp .env.example .env
   # Then edit .env and add your AI_API_KEY
   ```
5. Run the app:
   ```bash
   python app.py
   ```
6. Codespaces will prompt you to open the forwarded port. Click **Open in Browser**.

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serve the main page |
| `GET` | `/api/conversations` | List all conversations |
| `POST` | `/api/conversations` | Create a new conversation |
| `GET` | `/api/conversations/<id>` | Get a conversation + messages |
| `DELETE` | `/api/conversations/<id>` | Delete a conversation |
| `POST` | `/api/chat` | Send a question, get AI answer |
| `GET` | `/api/search?q=<query>` | Search conversations |
| `GET` | `/api/status` | Check AI configuration status |

---

## How It Works

```
Student types a question
        ↓
Flask receives POST /api/chat
        ↓
Load conversation history from SQLite
        ↓
Send history + question to AI API (OpenAI-compatible)
        ↓
Receive AI answer
        ↓
Save question + answer to SQLite
        ↓
Return answer to browser
        ↓
JavaScript renders the response bubble
```

---

## Database

The SQLite database is created automatically at `database/assistant.db` on first run.

**`conversations` table**

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Primary key |
| `title` | TEXT | Auto-generated from first question |
| `created_at` | TEXT | Creation timestamp (UTC) |
| `updated_at` | TEXT | Last message timestamp (UTC) |

**`messages` table**

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Primary key |
| `conversation_id` | INTEGER | Foreign key → conversations |
| `role` | TEXT | `user` or `assistant` |
| `content` | TEXT | Message text |
| `created_at` | TEXT | Timestamp (UTC) |

Deleting a conversation automatically deletes all its messages (CASCADE).

---

## AI Integration

- The `ai_service.py` module uses the `openai` Python package with a configurable `base_url`.
- This means it works with **OpenAI**, **Azure OpenAI**, or any OpenAI-compatible provider.
- The API key is read exclusively from the `AI_API_KEY` environment variable — never from code.
- If no key is configured, the application continues to work (database, search, history) but shows a clear setup message when a chat is attempted.

---

## Security

- API keys are read from environment variables only.
- `.env` is listed in `.gitignore`.
- All database queries use parameterized statements (no SQL injection risk).
- User input is HTML-escaped before rendering.
- Internal error details are never exposed to the UI.

---

## Future Improvements

- ☁️ Deploy to AWS (Elastic Beanstalk or EC2 + Gunicorn + Nginx)
- 🐘 Replace SQLite with PostgreSQL or Oracle Database for production
- 👤 User authentication (login, per-user conversation history)
- 📎 File upload (PDF, image) for AI to analyse
- 📝 AI study plan generator
- 🧪 Quiz generation from conversation content
- 🎙️ Voice input via Web Speech API
- 📊 Learning analytics dashboard
- 🌙 Dark mode toggle

---

## License

MIT License — free to use, modify, and distribute.
