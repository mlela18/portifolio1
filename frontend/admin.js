// Admin panel — loads messages from the backend and handles replies.

const API_BASE = window.API_BASE || 'http://127.0.0.1:5000/api';

const statusDiv     = document.getElementById('adminStatus');
const messagesList  = document.getElementById('messagesList');

// ─── Helpers ──────────────────────────────────────────────────────────────────

async function apiFetch(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const response = await fetch(url, {
    headers: { 'Content-Type': 'application/json' },
    ...options
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || `Server error ${response.status}`);
  }
  return data;
}

// ─── Load messages ─────────────────────────────────────────────────────────────

async function loadMessages() {
  statusDiv.textContent  = 'Loading messages…';
  statusDiv.style.color  = 'blue';
  messagesList.innerHTML = '';

  try {
    const data = await apiFetch('/contact/all');

    statusDiv.textContent = `${data.count} message(s) loaded.`;
    statusDiv.style.color = 'green';

    if (data.count === 0) {
      messagesList.innerHTML = '<p style="text-align:center; color:#aaa;">No messages received yet.</p>';
      return;
    }

    messagesList.innerHTML = data.contacts.map(contact => `
      <div class="message-card">
        <h3>${escapeHtml(contact.name)}</h3>
        <p><strong>Email:</strong> ${escapeHtml(contact.email)}</p>
        <p><strong>Message:</strong> ${escapeHtml(contact.message)}</p>
        <p><strong>Received:</strong> ${formatDate(contact.timestamp)}</p>
        ${contact.reply
          ? `<p><strong>✓ Replied:</strong> ${escapeHtml(contact.reply)} <em style="color:#aaa;">(${formatDate(contact.reply_timestamp)})</em></p>`
          : `<p><strong>Reply:</strong> <em style="color:#aaa;">No reply yet</em></p>`
        }
        <form class="reply-form" data-id="${contact.id}">
          <textarea name="reply" placeholder="Write your reply here…" required></textarea>
          <button type="submit">Send Reply</button>
          <div class="reply-status"></div>
        </form>
      </div>
    `).join('');

  } catch (error) {
    statusDiv.textContent = `Error: ${error.message}`;
    statusDiv.style.color = 'red';
    console.error('loadMessages failed:', error);
  }
}

// ─── Send reply ────────────────────────────────────────────────────────────────

document.addEventListener('submit', async function(event) {
  if (!event.target.matches('.reply-form')) return;

  event.preventDefault();
  const form       = event.target;
  const contactId  = parseInt(form.dataset.id, 10);
  const reply      = form.reply.value.trim();
  const statusEl   = form.querySelector('.reply-status');

  if (!reply) {
    statusEl.style.color  = 'red';
    statusEl.textContent  = 'Reply text is required.';
    return;
  }

  statusEl.style.color  = 'blue';
  statusEl.textContent  = 'Sending reply…';

  try {
    const data = await apiFetch('/contact/reply', {
      method: 'POST',
      body: JSON.stringify({ id: contactId, reply })
    });

    statusEl.style.color  = 'green';
    statusEl.textContent  = data.email_status || 'Reply saved successfully.';
    form.reset();

    // Reload list so the reply shows up
    setTimeout(loadMessages, 800);

  } catch (error) {
    statusEl.style.color  = 'red';
    statusEl.textContent  = `Error: ${error.message}`;
    console.error('Reply failed:', error);
  }
});

// ─── Utilities ────────────────────────────────────────────────────────────────

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function formatDate(iso) {
  if (!iso) return '—';
  try {
    return new Date(iso).toLocaleString();
  } catch {
    return iso;
  }
}

// ─── Boot ─────────────────────────────────────────────────────────────────────

loadMessages();
