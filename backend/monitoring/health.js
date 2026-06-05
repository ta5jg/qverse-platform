// Q-Verse V9 System Health
async function getSystemHealth(services) {
    const status = {};
    for (const [name, check] of Object.entries(services)) {
        try {
            status[name] = await check();
        } catch (e) {
            status[name] = 'unhealthy';
        }
    }
    return status;
}
module.exports = { getSystemHealth };
