// Q-Verse V9 API Middleware Wrapper
module.exports = function middlewareWrapper(middleware) {
    return (req, res, next) => middleware(req, res, next);
};
