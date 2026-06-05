// Q-Verse V9 Scheduler Jobs
function registerHealthJob(scheduler, healthCheck) {
    scheduler.schedule('*/5 * * * *', async () => {
        await healthCheck();
    });
}
function registerBackupJob(scheduler, backupFn) {
    scheduler.schedule('0 3 * * *', async () => {
        await backupFn();
    });
}
module.exports = { registerHealthJob, registerBackupJob };
