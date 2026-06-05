// Q-Verse V9 API Key Auth Middleware
module.exports = function apiKeyAuth(req, res, next) {
    const apiKey = req.header('x-api-key');
    if (!apiKey || apiKey !== process.env.API_KEY) {
        return res.status(401).json({ error: 'Invalid API Key' });
    }
    next();
};
