# Auto-generated: CSS for AI Student Assistant
CONTENT = """/* ─────────────────────────────────────────────────────────────────────────
   AI Student Assistant — Stylesheet
   Professional, responsive, accessible design
   ───────────────────────────────────────────────────────────────────────── */

/* ── Reset & base ───────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --sidebar-w:       300px;
  --header-h:        64px;
  --input-h:         100px;

  /* Colour palette */
  --c-bg:            #f0f4f8;
  --c-surface:       #ffffff;
  --c-sidebar:       #1e293b;
  --c-sidebar-hover: #334155;
  --c-sidebar-active:#3b82f6;
  --c-border:        #e2e8f0;
  --c-text:          #1e293b;
  --c-text-muted:    #64748b;
  --c-text-sidebar:  #cbd5e1;
  --c-primary:       #3b82f6;
  --c-primary-dark:  #2563eb;
  --c-danger:        #ef4444;
  --c-danger-dark:   #dc2626;
  --c-success:       #22c55e;
  --c-warning-bg:    #fffbeb;
  --c-warning-border:#f59e0b;
  --c-warning-text:  #92400e;
  --c-user-bubble:   #3b82f6;
  --c-ai-bubble:     #ffffff;
  --c-ai-border:     #e2e8f0;
  --c-code-bg:       #1e293b;
  --c-code-text:     #e2e8f0;

  /* Shadows */
  --shadow-sm:  0 1px 3px rgba(0,0,0,.08);
  --shadow-md:  0 4px 12px rgba(0,0,0,.10);
  --shadow-lg:  0 8px 30px rgba(0,0,0,.14);

  /* Transitions */
  --t-fast:  0.15s ease;
  --t-med:   0.25s ease;

  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  font-size: 15px;
  line-height: 1.6;
  color: var(--c-text);
}

html, body { height: 100%; overflow: hidden; }

body { background: var(--c-bg); display: flex; }

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
.sidebar {
  width: var(--sidebar-w);
  min-width: var(--sidebar-w);
  background: var(--c-sidebar);
  display: flex;
  flex-direction: column;
  height: 100vh;
  position: relative;
  z-index: 20;
  transition: transform var(--t-med);
}

.sidebar-header {
  padding: 20px 16px 16px;
  border-bottom: 1px solid rgba(255,255,255,.07);
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.app-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.app-icon { font-size: 28px; flex-shrink: 0; }

.app-name {
  font-size: 15px;
  font-weight: 700;
  color: #fff;
  line-height: 1.2;
}

.app-tagline {
  font-size: 11px;
  color: var(--c-text-sidebar);
  margin-top: 2px;
}

.btn-new-chat {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 10px 16px;
  background: var(--c-primary);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background var(--t-fast), transform var(--t-fast);
  font-family: inherit;
}

.btn-new-chat:hover  { background: var(--c-primary-dark); }
.btn-new-chat:active { transform: scale(0.97); }

/* ── Search ──────────────────────────────────────────────────────────────── */
.search-wrap { padding: 12px 16px; }

.search-inner {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 11px;
  color: var(--c-text-sidebar);
  pointer-events: none;
  flex-shrink: 0;
}

.search-input {
  width: 100%;
  padding: 9px 36px 9px 36px;
  background: rgba(255,255,255,.08);
  border: 1px solid rgba(255,255,255,.10);
  border-radius: 8px;
  color: #fff;
  font-size: 13px;
  font-family: inherit;
  transition: border-color var(--t-fast), background var(--t-fast);
  outline: none;
}

.search-input::placeholder { color: #94a3b8; }

.search-input:focus {
  background: rgba(255,255,255,.12);
  border-color: var(--c-primary);
}

.btn-clear-search {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 13px;
  padding: 2px;
  line-height: 1;
}

.btn-clear-search:hover { color: #fff; }

/* ── Conversation list ───────────────────────────────────────────────────── */
.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px 10px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.conversation-list::-webkit-scrollbar { width: 4px; }
.conversation-list::-webkit-scrollbar-track { background: transparent; }
.conversation-list::-webkit-scrollbar-thumb { background: rgba(255,255,255,.15); border-radius: 4px; }

.list-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 40px 20px;
  color: #64748b;
  font-size: 13px;
  text-align: center;
}

.list-empty span { font-size: 28px; }

/* Individual conversation item */
.conv-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: background var(--t-fast);
  position: relative;
  group: true;
}

.conv-item:hover { background: var(--c-sidebar-hover); }

.conv-item.active {
  background: rgba(59, 130, 246, .25);
  border-left: 3px solid var(--c-primary);
  padding-left: 9px;
}

.conv-icon { font-size: 15px; flex-shrink: 0; }

.conv-details { flex: 1; min-width: 0; }

.conv-title {
  font-size: 13px;
  font-weight: 500;
  color: #e2e8f0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.4;
}

.conv-item.active .conv-title { color: #fff; }

.conv-date {
  font-size: 11px;
  color: #64748b;
  margin-top: 2px;
}

.btn-conv-delete {
  flex-shrink: 0;
  background: none;
  border: none;
  color: #475569;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  opacity: 0;
  transition: opacity var(--t-fast), color var(--t-fast), background var(--t-fast);
  font-size: 14px;
  line-height: 1;
}

.conv-item:hover .btn-conv-delete { opacity: 1; }
.btn-conv-delete:hover { color: var(--c-danger); background: rgba(239,68,68,.15); }

/* ── Sidebar toggle (mobile) ─────────────────────────────────────────────── */
.btn-sidebar-toggle {
  display: none;
  position: fixed;
  top: 14px;
  left: 14px;
  z-index: 30;
  background: var(--c-sidebar);
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 8px;
  cursor: pointer;
  box-shadow: var(--shadow-md);
}

/* ── Main area ───────────────────────────────────────────────────────────── */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  background: var(--c-bg);
  position: relative;
}

/* ── Banner ──────────────────────────────────────────────────────────────── */
.banner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  font-size: 13px;
  flex-shrink: 0;
}

.banner-warning {
  background: var(--c-warning-bg);
  border-bottom: 1px solid var(--c-warning-border);
  color: var(--c-warning-text);
}

.banner svg { flex-shrink: 0; }

.banner span { flex: 1; }

.banner code {
  background: rgba(0,0,0,.08);
  padding: 1px 5px;
  border-radius: 4px;
  font-size: 12px;
  font-family: 'Courier New', monospace;
}

.btn-banner-close {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--c-warning-text);
  font-size: 16px;
  padding: 2px 6px;
  border-radius: 4px;
  opacity: 0.7;
}

.btn-banner-close:hover { opacity: 1; }

/* ── Chat header ──────────────────────────────────────────────────────────── */
.chat-header {
  padding: 16px 24px 12px;
  border-bottom: 1px solid var(--c-border);
  background: var(--c-surface);
  flex-shrink: 0;
}

.chat-title {
  font-size: 17px;
  font-weight: 600;
  color: var(--c-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-subtitle {
  font-size: 12px;
  color: var(--c-text-muted);
  margin-top: 2px;
}

/* ── Messages area ───────────────────────────────────────────────────────── */
.messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  scroll-behavior: smooth;
}

.messages::-webkit-scrollbar { width: 6px; }
.messages::-webkit-scrollbar-track { background: transparent; }
.messages::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 6px; }

/* ── Welcome state ───────────────────────────────────────────────────────── */
.welcome-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 16px;
  flex: 1;
  padding: 40px 20px;
  min-height: 300px;
}

.welcome-icon { font-size: 56px; }

.welcome-state h2 {
  font-size: 22px;
  font-weight: 700;
  color: var(--c-text);
}

.welcome-state p {
  font-size: 15px;
  color: var(--c-text-muted);
  max-width: 400px;
}

.welcome-suggestions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  max-width: 600px;
  margin-top: 8px;
}

.suggestion-chip {
  padding: 9px 16px;
  background: var(--c-surface);
  border: 1px solid var(--c-border);
  border-radius: 20px;
  font-size: 13px;
  color: var(--c-text);
  cursor: pointer;
  transition: background var(--t-fast), border-color var(--t-fast), transform var(--t-fast);
  font-family: inherit;
}

.suggestion-chip:hover {
  background: #eff6ff;
  border-color: var(--c-primary);
  color: var(--c-primary);
  transform: translateY(-1px);
}

/* ── Message bubbles ─────────────────────────────────────────────────────── */
.message {
  display: flex;
  gap: 12px;
  max-width: 820px;
  animation: fadeUp 0.2s ease;
}

@keyframes fadeUp {
  from { opacity: 0; transform: translateY(8px); }
  to   { opacity: 1; transform: translateY(0); }
}

.message.user-msg  { flex-direction: row-reverse; align-self: flex-end; }
.message.ai-msg    { flex-direction: row; align-self: flex-start; }

.msg-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
  margin-top: 2px;
}

.user-msg .msg-avatar { background: var(--c-primary); }
.ai-msg   .msg-avatar { background: #f1f5f9; border: 1px solid var(--c-border); }

.msg-bubble {
  max-width: calc(100% - 54px);
  padding: 12px 16px;
  border-radius: 16px;
  font-size: 14.5px;
  line-height: 1.65;
  position: relative;
}

.user-msg .msg-bubble {
  background: var(--c-user-bubble);
  color: #fff;
  border-bottom-right-radius: 4px;
}

.ai-msg .msg-bubble {
  background: var(--c-ai-bubble);
  color: var(--c-text);
  border: 1px solid var(--c-ai-border);
  border-bottom-left-radius: 4px;
  box-shadow: var(--shadow-sm);
}

.msg-time {
  font-size: 11px;
  margin-top: 5px;
  opacity: 0.55;
}

.user-msg .msg-time { text-align: right; color: #fff; }
.ai-msg   .msg-time { color: var(--c-text-muted); }

/* Markdown-like content inside AI bubbles */
.msg-bubble h1, .msg-bubble h2, .msg-bubble h3 {
  font-size: 15px;
  font-weight: 700;
  margin: 14px 0 6px;
  color: var(--c-text);
}

.msg-bubble h1:first-child,
.msg-bubble h2:first-child,
.msg-bubble h3:first-child { margin-top: 0; }

.msg-bubble p { margin-bottom: 10px; }
.msg-bubble p:last-child { margin-bottom: 0; }

.msg-bubble ul, .msg-bubble ol {
  padding-left: 22px;
  margin-bottom: 10px;
}

.msg-bubble li { margin-bottom: 4px; }

.msg-bubble code {
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
  font-family: 'Courier New', Consolas, monospace;
  color: #0f172a;
}

.msg-bubble pre {
  background: var(--c-code-bg);
  color: var(--c-code-text);
  padding: 14px 16px;
  border-radius: 10px;
  overflow-x: auto;
  margin: 10px 0;
  font-size: 13px;
  line-height: 1.6;
}

.msg-bubble pre code {
  background: none;
  color: inherit;
  padding: 0;
  font-size: inherit;
}

.msg-bubble strong { font-weight: 600; }

.msg-bubble blockquote {
  border-left: 3px solid var(--c-primary);
  padding-left: 14px;
  color: var(--c-text-muted);
  font-style: italic;
  margin: 10px 0;
}

/* ── Typing indicator ────────────────────────────────────────────────────── */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 24px 0;
  animation: fadeUp 0.2s ease;
}

.typing-bubble {
  background: var(--c-ai-bubble);
  border: 1px solid var(--c-ai-border);
  border-radius: 14px;
  padding: 10px 14px;
  display: flex;
  gap: 5px;
  align-items: center;
}

.dot {
  width: 8px;
  height: 8px;
  background: var(--c-text-muted);
  border-radius: 50%;
  animation: bounce 1.2s infinite;
}

.dot:nth-child(2) { animation-delay: 0.2s; }
.dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes bounce {
  0%, 60%, 100% { transform: translateY(0); }
  30%           { transform: translateY(-6px); }
}

.typing-text { font-size: 12px; color: var(--c-text-muted); }

/* ── Input area ──────────────────────────────────────────────────────────── */
.input-area {
  border-top: 1px solid var(--c-border);
  padding: 14px 20px 10px;
  background: var(--c-surface);
  flex-shrink: 0;
}

.input-wrap {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  background: #f8fafc;
  border: 1.5px solid var(--c-border);
  border-radius: 14px;
  padding: 8px 8px 8px 14px;
  transition: border-color var(--t-fast);
}

.input-wrap:focus-within { border-color: var(--c-primary); background: #fff; }

.question-input {
  flex: 1;
  background: none;
  border: none;
  outline: none;
  resize: none;
  font-size: 14.5px;
  font-family: inherit;
  line-height: 1.6;
  color: var(--c-text);
  max-height: 160px;
  overflow-y: auto;
}

.question-input::placeholder { color: #94a3b8; }

.btn-send {
  width: 40px;
  height: 40px;
  background: var(--c-primary);
  color: #fff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background var(--t-fast), transform var(--t-fast), opacity var(--t-fast);
  flex-shrink: 0;
}

.btn-send:hover:not(:disabled)  { background: var(--c-primary-dark); }
.btn-send:active:not(:disabled) { transform: scale(0.93); }

.btn-send:disabled {
  background: #94a3b8;
  cursor: not-allowed;
  opacity: 0.65;
}

.input-hint {
  font-size: 11px;
  color: #94a3b8;
  margin-top: 6px;
  text-align: center;
}

.input-hint kbd {
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  padding: 1px 5px;
  font-size: 10px;
  font-family: inherit;
}

/* ── Error message ───────────────────────────────────────────────────────── */
.msg-error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
  border-radius: 10px;
  padding: 12px 16px;
  font-size: 13.5px;
  max-width: 600px;
  align-self: center;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  animation: fadeUp 0.2s ease;
}

.msg-error-icon { font-size: 18px; flex-shrink: 0; }

/* ── Delete modal ────────────────────────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  animation: fadeIn 0.15s ease;
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.modal {
  background: #fff;
  border-radius: 16px;
  padding: 28px 32px;
  max-width: 420px;
  width: 90%;
  text-align: center;
  box-shadow: var(--shadow-lg);
  animation: slideUp 0.2s ease;
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}

.modal-icon  { font-size: 40px; margin-bottom: 12px; }
.modal h3    { font-size: 18px; font-weight: 700; margin-bottom: 8px; }
.modal p     { font-size: 14px; color: var(--c-text-muted); margin-bottom: 24px; }

.modal-actions { display: flex; gap: 12px; justify-content: center; }

.btn-cancel {
  padding: 10px 24px;
  background: #f1f5f9;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: background var(--t-fast);
}

.btn-cancel:hover { background: #e2e8f0; }

.btn-delete-confirm {
  padding: 10px 24px;
  background: var(--c-danger);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: background var(--t-fast);
}

.btn-delete-confirm:hover { background: var(--c-danger-dark); }

/* ── Toast notification ──────────────────────────────────────────────────── */
.toast {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%) translateY(20px);
  background: #1e293b;
  color: #fff;
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 13.5px;
  opacity: 0;
  transition: opacity 0.25s ease, transform 0.25s ease;
  pointer-events: none;
  z-index: 200;
  white-space: nowrap;
  box-shadow: var(--shadow-lg);
}

.toast.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0);
}

/* ── Responsive ──────────────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    transform: translateX(-100%);
    z-index: 25;
  }

  .sidebar.open { transform: translateX(0); }

  .btn-sidebar-toggle { display: flex; }

  .chat-header { padding-left: 58px; }

  .messages { padding: 16px; }

  .input-area { padding: 10px 14px 8px; }

  .message { max-width: 100%; }

  .modal { padding: 24px 20px; }
}

@media (max-width: 480px) {
  .welcome-state h2 { font-size: 18px; }
  .welcome-suggestions { flex-direction: column; align-items: stretch; }
  .suggestion-chip { text-align: left; }
}
"""
