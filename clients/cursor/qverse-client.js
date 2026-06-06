// Q-Verse Cursor Client V10.1+
const DEFAULT_ENDPOINT = process.env.QVERSE_API_URL || 'https://api.q-verse.io/agents/chat';

async function askQVerse(message, options = {}) {
  const payload = {
    message,
    source: options.source || 'cursor',
    user_id: options.user_id || process.env.USER || 'cursor-user',
    username: options.username || process.env.USER || 'cursor-user',
    context: options.context || {}
  };

  const response = await fetch(options.endpoint || DEFAULT_ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`Q-Verse API error: ${response.status} ${response.statusText}`);
  }

  return await response.json();
}

module.exports = { askQVerse };
