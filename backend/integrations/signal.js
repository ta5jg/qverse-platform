// Q-Verse V9 Signal Integration
async function sendSignalMessage(signalApiUrl, number, message) {
    const fetch = require('node-fetch');
    await fetch(signalApiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ number, message })
    });
}
module.exports = { sendSignalMessage };
