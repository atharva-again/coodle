import aiosqlite
import logging
from config import DATABASE_PATH

logger = logging.getLogger(__name__)


async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sent_notifications (
                deadline_id TEXT PRIMARY KEY,
                title TEXT,
                due_date TIMESTAMP,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()
        logger.info("Database initialized")


async def is_notified(deadline_id: str) -> bool:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT 1 FROM sent_notifications WHERE deadline_id = ?", (deadline_id,)
        ) as cursor:
            return await cursor.fetchone() is not None


async def mark_as_notified(deadline_id: str, title: str, due_date: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT INTO sent_notifications (deadline_id, title, due_date) VALUES (?, ?, ?)",
            (deadline_id, title, due_date),
        )
        await db.commit()
