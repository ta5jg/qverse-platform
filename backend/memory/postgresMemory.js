// Q-Verse V9 PostgresMemory
class PostgresMemory {
    constructor(pool) {
        this.pool = pool;
    }
    async saveMemory(userId, memory) {
        await this.pool.query(
            'INSERT INTO memories(user_id, memory, created_at) VALUES ($1, $2, NOW())',
            [userId, memory]
        );
    }
    async getMemories(userId) {
        const res = await this.pool.query(
            'SELECT memory, created_at FROM memories WHERE user_id = $1 ORDER BY created_at DESC',
            [userId]
        );
        return res.rows;
    }
}
module.exports = PostgresMemory;
