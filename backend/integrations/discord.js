// Q-Verse V9 Discord Integration
async function sendDiscordMessage(webhookUrl, content) {
    const fetch = require('node-fetch');
    await fetch(webhookUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content })
    });
}
module.exports = { sendDiscordMessage };
