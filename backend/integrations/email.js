// Q-Verse V9 Email Integration
async function sendEmail(transporter, options) {
    await transporter.sendMail(options);
}
module.exports = { sendEmail };
