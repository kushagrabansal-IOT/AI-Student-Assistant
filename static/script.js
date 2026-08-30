/**
 * AI Student Assistant — Frontend Script
 * Handles all UI interactions via fetch() calls to the Flask API.
 * No external libraries required — vanilla JS only.
 */

'use strict';

// ── State ─────────────────────────────────────────────────────────────────
let currentConvId  = null;   // Active conversation ID (null = no conversation)
let pendingRequest = false;  // Prevent double-sends
let deleteTargetId = null;   // Conversation pending deletion
let searchTimeout  = null;   // Debounce handle

// ── DOM references ─────────────────────────────────────────────────────────
const messagesEl      = document.getElementById('messages');
const questionInput   = document.getElementById('question-input');
const btnSend         = document.getElementById('btn-send');
const btnNewChat      = document.getElementById('btn-new-chat');
const convList        = document.getElementById('conversation-list');
const listEmpty       = document.getElementById('list-empty');
const searchInput     = document.getElementById('search-input');
const btnClearSearch  = document.getElementById('btn-clear-search');
const typingIndicator = document.getElementById('typing-indicator');
const chatTitle       = document.getElementById('chat-title');
const chatSubtitle    = document.getElementById('chat-subtitle');
const welcomeState    = document.getElementById('welcome-state');
const deleteModal     = document.getElementById('delete-modal');
const btnDeleteConfirm= document.getElementById('btn-delete-confirm');
const btnDeleteCancel = document.getElementById('btn-delete-cancel');
const toast           = document.getElementById('toast');
const btnSidebarToggle= document.getElementById('btn-sidebar-toggle');
const sidebar         = document.getElementById('sidebar');

// ═══════════════════════════════════════════════════════════════════════════
// INITIALISATION
// ═══════════════════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
  loadConversationList();
  bindEvents();
  questionInput.focus();
});

function bindEvents() {
  // Send on button click
  btnSend.addEventListener('click', sendMessage);

  // Send on Enter (Shift+Enter = newline)
  questionInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // Auto-resize textarea
  questionInput.addEventListener('input', () => {
    questionInput.style.height = 'auto';
    questionInput.style.height = Math.min(questionInput.scrollHeight, 160) + 'px';
  });

  // New chat
  btnNewChat.addEventListener('click', startNewChat);

  // Search with 300ms debounce
  searchInput.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    const q = searchInput.value.trim();
    btnClearSearch.style.display = q ? 'block' : 'none';
    searchTimeout = setTimeout(() => runSearch(q), 300);
  });

  // Clear search
  btnClearSearch.addEventListener('click', () => {
    searchInput.value = '';
    btnClearSearch.style.display = 'none';
    loadConversationList();
    searchInput.focus();
  });

  // Delete modal
  btnDeleteConfirm.addEventListener('click', confirmDelete);
  btnDeleteCancel.addEventListener('click',  closeDeleteModal);
  deleteModal.addEventListener('click', e => {
    if (e.target === deleteModal) closeDeleteModal();
  });

  // Sidebar toggle (mobile)
  btnSidebarToggle.addEventListener('click', () => {
    sidebar.classList.toggle('open');
  });

  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', e => {
    if (window.innerWidth <= 768 &&
        sidebar.classList.contains('open') &&
        !sidebar.contains(e.target) &&
        e.target !== btnSidebarToggle) {
      sidebar.classList.remove('open');
    }
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// SEND MESSAGE
// ═══════════════════════════════════════════════════════════════════════════

async function sendMessage() {
  const question = questionInput.value.trim();

  if (!question)        { shakeInput(); return; }
  if (pendingRequest)   { return; }
  if (question.length > 10000) {
    showToast('Message too long (max 10,000 characters)', 'error');
    return;
  }

  pendingRequest = true;
  setInputDisabled(true);

  // Render user bubble immediately
  appendMessage('user', question);
  questionInput.value = '';
  questionInput.style.height = 'auto';
  hideWelcome();
  showTyping(true);
  scrollToBottom();

  try {
    const res  = await fetch('/api/chat', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify({ question, conversation_id: currentConvId }),
    });

    const data = await res.json();
    showTyping(false);

    if (!res.ok) {
      if (data.error === 'ai_not_configured') {
        appendError(
          '⚙️ AI not configured',
          data.message ||
          'Set the AI_API_KEY environment variable. See .env.example for instructions.'
        );
      } else if (data.error === 'ai_error') {
        appendError('🤖 AI error', data.message || 'The AI service returned an error.');
      } else {
        appendError('❌ Error', data.error || 'Something went wrong. Please try again.');
      }
      return;
    }

    // Update state with the conversation returned from server
    if (!currentConvId && data.conversation_id) {
      currentConvId = data.conversation_id;
    }

    appendMessage('assistant', data.answer);

    if (data.conversation) {
      setChatHeader(data.conversation.title);
    }

    // Refresh sidebar to show new/updated conversation
    await loadConversationList();
    highlightActiveConv(currentConvId);

  } catch (err) {
    showTyping(false);
    appendError('🌐 Network error', 'Could not reach the server. Check your connection and try again.');
    console.error('sendMessage error:', err);
  } finally {
    pendingRequest = false;
    setInputDisabled(false);
    questionInput.focus();
    scrollToBottom();
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// NEW CHAT
// ═══════════════════════════════════════════════════════════════════════════

function startNewChat() {
  currentConvId = null;
  clearMessages();
  showWelcome();
  setChatHeader('Start a New Conversation', 'Ask me anything — I\'m here to help you learn.');
  highlightActiveConv(null);
  questionInput.focus();
  if (window.innerWidth <= 768) sidebar.classList.remove('open');
}

// ═══════════════════════════════════════════════════════════════════════════
// LOAD CONVERSATION LIST
// ═══════════════════════════════════════════════════════════════════════════

async function loadConversationList() {
  try {
    const res  = await fetch('/api/conversations');
    const data = await res.json();
    renderConvList(data.conversations || []);
  } catch (err) {
    console.error('loadConversationList error:', err);
  }
}

function renderConvList(conversations) {
  // Remove all conv items (keep the empty-state div)
  convList.querySelectorAll('.conv-item').forEach(el => el.remove());

  if (conversations.length === 0) {
    listEmpty.style.display = 'flex';
    return;
  }

  listEmpty.style.display = 'none';

  conversations.forEach(conv => {
    const el = document.createElement('div');
    el.className = 'conv-item';
    el.dataset.id = conv.id;
    if (conv.id === currentConvId) el.classList.add('active');

    el.innerHTML = `
      <span class="conv-icon">💬</span>
      <div class="conv-details">
        <div class="conv-title" title="${escapeHtml(conv.title)}">${escapeHtml(conv.title)}</div>
        <div class="conv-date">${formatDate(conv.updated_at)}</div>
      </div>
      <button class="btn-conv-delete" title="Delete conversation" data-id="${conv.id}">🗑️</button>
    `;

    // Click conversation item → load it
    el.addEventListener('click', e => {
      if (e.target.classList.contains('btn-conv-delete')) return;
      loadConversation(conv.id);
      if (window.innerWidth <= 768) sidebar.classList.remove('open');
    });

    // Click delete button → open modal
    el.querySelector('.btn-conv-delete').addEventListener('click', e => {
      e.stopPropagation();
      openDeleteModal(conv.id);
    });

    convList.appendChild(el);
  });
}

// ═══════════════════════════════════════════════════════════════════════════
// LOAD A SINGLE CONVERSATION
// ═══════════════════════════════════════════════════════════════════════════

async function loadConversation(convId) {
  if (pendingRequest) return;

  try {
    const res  = await fetch(`/api/conversations/${convId}`);
    if (!res.ok) { showToast('Could not load conversation', 'error'); return; }

    const data = await res.json();
    currentConvId = convId;

    clearMessages();
    hideWelcome();
    setChatHeader(data.conversation.title);
    highlightActiveConv(convId);

    if (data.messages.length === 0) {
      showWelcome();
    } else {
      data.messages.forEach(msg => appendMessage(msg.role, msg.content, false));
    }

    scrollToBottom(false);
  } catch (err) {
    showToast('Network error loading conversation', 'error');
    console.error('loadConversation error:', err);
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// SEARCH
// ═══════════════════════════════════════════════════════════════════════════

async function runSearch(query) {
  if (!query) { loadConversationList(); return; }

  try {
    const res  = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    renderConvList(data.conversations || []);
  } catch (err) {
    console.error('search error:', err);
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// DELETE CONVERSATION
// ═══════════════════════════════════════════════════════════════════════════

function openDeleteModal(convId) {
  deleteTargetId = convId;
  deleteModal.style.display = 'flex';
}

function closeDeleteModal() {
  deleteModal.style.display = 'none';
  deleteTargetId = null;
}

async function confirmDelete() {
  if (!deleteTargetId) return;

  const idToDelete = deleteTargetId;
  closeDeleteModal();

  try {
    const res = await fetch(`/api/conversations/${idToDelete}`, { method: 'DELETE' });
    if (!res.ok) { showToast('Could not delete conversation', 'error'); return; }

    showToast('Conversation deleted');

    // If the deleted conversation was active, start a new chat
    if (idToDelete === currentConvId) {
      startNewChat();
    } else {
      await loadConversationList();
      if (currentConvId) highlightActiveConv(currentConvId);
    }
  } catch (err) {
    showToast('Network error — could not delete', 'error');
    console.error('confirmDelete error:', err);
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// RENDER HELPERS
// ═══════════════════════════════════════════════════════════════════════════

function appendMessage(role, content, animate = true) {
  const isUser = role === 'user';

  const wrapper = document.createElement('div');
  wrapper.className = `message ${isUser ? 'user-msg' : 'ai-msg'}`;
  if (!animate) wrapper.style.animation = 'none';

  const avatar = document.createElement('div');
  avatar.className = 'msg-avatar';
  avatar.textContent = isUser ? '👤' : '🤖';

  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';

  const contentDiv = document.createElement('div');
  contentDiv.className = 'msg-content';

  if (isUser) {
    // User messages: plain text (escaped)
    contentDiv.textContent = content;
  } else {
    // AI messages: render basic markdown
    contentDiv.innerHTML = renderMarkdown(content);
  }

  const timeDiv = document.createElement('div');
  timeDiv.className = 'msg-time';
  timeDiv.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  bubble.appendChild(contentDiv);
  bubble.appendChild(timeDiv);
  wrapper.appendChild(avatar);
  wrapper.appendChild(bubble);
  messagesEl.appendChild(wrapper);
}

function appendError(title, detail) {
  const el = document.createElement('div');
  el.className = 'msg-error';
  el.innerHTML = `
    <span class="msg-error-icon">⚠️</span>
    <div>
      <strong>${escapeHtml(title)}</strong>
      <p style="margin:4px 0 0; font-size:13px; opacity:.85;">${escapeHtml(detail)}</p>
    </div>
  `;
  messagesEl.appendChild(el);
}

function clearMessages() {
  // Remove all children except the welcome state
  Array.from(messagesEl.children).forEach(child => {
    if (child.id !== 'welcome-state') child.remove();
  });
}

function hideWelcome() {
  if (welcomeState) welcomeState.style.display = 'none';
}

function showWelcome() {
  if (welcomeState) welcomeState.style.display = 'flex';
}

function setChatHeader(title, subtitle = null) {
  if (chatTitle)    chatTitle.textContent = title || 'Conversation';
  if (chatSubtitle && subtitle !== null) chatSubtitle.textContent = subtitle;
}

function highlightActiveConv(convId) {
  convList.querySelectorAll('.conv-item').forEach(el => {
    el.classList.toggle('active', parseInt(el.dataset.id) === convId);
  });
}

function showTyping(visible) {
  typingIndicator.style.display = visible ? 'flex' : 'none';
  if (visible) scrollToBottom();
}

function setInputDisabled(disabled) {
  questionInput.disabled = disabled;
  btnSend.disabled       = disabled;
}

function scrollToBottom(smooth = true) {
  setTimeout(() => {
    messagesEl.scrollTo({
      top:      messagesEl.scrollHeight,
      behavior: smooth ? 'smooth' : 'auto',
    });
  }, 50);
}

function shakeInput() {
  questionInput.style.animation = 'none';
  void questionInput.offsetWidth;   // reflow
  questionInput.style.animation = 'shake 0.3s ease';
  setTimeout(() => { questionInput.style.animation = ''; }, 350);
}

// ═══════════════════════════════════════════════════════════════════════════
// TOAST NOTIFICATIONS
// ═══════════════════════════════════════════════════════════════════════════

let toastTimeout = null;

function showToast(message, type = 'success') {
  toast.textContent = message;
  toast.style.background = type === 'error' ? '#b91c1c' : '#1e293b';
  toast.classList.add('show');
  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => toast.classList.remove('show'), 3000);
}

// ═══════════════════════════════════════════════════════════════════════════
// MARKDOWN RENDERER (lightweight, no external library)
// ═══════════════════════════════════════════════════════════════════════════

function renderMarkdown(text) {
  if (!text) return '';

  let html = escapeHtml(text);

  // Code blocks (``` ... ```)
  html = html.replace(/```[\w]*\n?([\s\S]*?)```/g, (_, code) =>
    `<pre><code>${code.trim()}</code></pre>`
  );

  // Inline code (`...`)
  html = html.replace(/`([^`\n]+)`/g, '<code>$1</code>');

  // Bold (**text** or __text__)
  html = html.replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/__([^_\n]+)__/g,      '<strong>$1</strong>');

  // Italic (*text* or _text_)
  html = html.replace(/\*([^*\n]+)\*/g, '<em>$1</em>');
  html = html.replace(/_([^_\n]+)_/g,   '<em>$1</em>');

  // Headings (### ## #)
  html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
  html = html.replace(/^## (.+)$/gm,  '<h2>$1</h2>');
  html = html.replace(/^# (.+)$/gm,   '<h1>$1</h1>');

  // Blockquote (> text)
  html = html.replace(/^&gt; (.+)$/gm, '<blockquote>$1</blockquote>');

  // Unordered list (- item or * item)
  html = html.replace(/^[*\-] (.+)$/gm, '<li>$1</li>');
  html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

  // Ordered list (1. item)
  html = html.replace(/^\d+\. (.+)$/gm, '<li>$1</li>');

  // Horizontal rule
  html = html.replace(/^---$/gm, '<hr>');

  // Paragraphs — double newline = paragraph break
  html = html
    .split(/\n{2,}/)
    .map(block => {
      block = block.trim();
      if (!block) return '';
      if (/^<(h[1-3]|ul|ol|li|pre|blockquote|hr)/.test(block)) return block;
      return `<p>${block.replace(/\n/g, '<br>')}</p>`;
    })
    .join('\n');

  return html;
}

// ═══════════════════════════════════════════════════════════════════════════
// UTILITIES
// ═══════════════════════════════════════════════════════════════════════════

function escapeHtml(str) {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  try {
    const d   = new Date(dateStr + (dateStr.includes('T') ? '' : ' UTC'));
    const now = new Date();
    const diffMs   = now - d;
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffDays === 0) {
      return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } else if (diffDays === 1) {
      return 'Yesterday';
    } else if (diffDays < 7) {
      return d.toLocaleDateString([], { weekday: 'long' });
    } else {
      return d.toLocaleDateString([], { month: 'short', day: 'numeric' });
    }
  } catch { return dateStr; }
}

// Suggestion chip handler (called inline from HTML)
function useSuggestion(btn) {
  questionInput.value = btn.textContent;
  questionInput.dispatchEvent(new Event('input'));
  sendMessage();
}

// Add shake animation via CSS injection (avoids extra CSS file)
const shakeStyle = document.createElement('style');
shakeStyle.textContent = `
  @keyframes shake {
    0%,100% { transform: translateX(0); }
    20%      { transform: translateX(-6px); }
    40%      { transform: translateX(6px); }
    60%      { transform: translateX(-4px); }
    80%      { transform: translateX(4px); }
  }
`;
document.head.appendChild(shakeStyle);
