// Q-Verse V9 Telegram Integration
async function sendTelegramMessage(botToken, chatId, text) {
    const fetch = require('node-fetch');
    const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
    await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: chatId, text })
    });
}
module.exports = { sendTelegramMessage };
