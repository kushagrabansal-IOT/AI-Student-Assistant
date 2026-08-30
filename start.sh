#!/bin/bash
# start.sh — Quick-start script for AI Student Assistant
# Usage: bash start.sh

set -e

echo ""
echo "🎓 AI Student Assistant — Startup"
echo "=================================="

# Check for .env file
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    cp .env.example .env
    echo "⚠️  Created .env from .env.example"
    echo "   → Add your AI_API_KEY to .env to enable AI responses."
    echo "   → The app will still run without it (AI responses disabled)."
  fi
fi

# Install dependencies if needed
if ! python3 -c "import flask" 2>/dev/null; then
  echo "📦 Installing dependencies..."
  pip install -r requirements.txt
fi

echo ""
echo "🚀 Starting Flask server on http://localhost:5000"
echo "   Press Ctrl+C to stop."
echo ""

python3 app.py
