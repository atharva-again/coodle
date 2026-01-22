import argparse
import asyncio
import datetime
import logging
from zoneinfo import ZoneInfo

from typing import Any, Protocol

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import CHECK_INTERVAL_HOURS, TIMEZONE
from database import init_db, is_notified, mark_as_notified
from mock_moodle_client import MockMoodleClient
from moodle_client import MoodleClient
from telegram_bot import TelegramNotifier


class MoodleClientInterface(Protocol):
    def get_upcoming_deadlines(self) -> list[dict[str, Any]]: ...


# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Global instances (will be initialized in main)
moodle: MoodleClientInterface | None = None
notifier = TelegramNotifier()


async def check_for_deadlines():
    """Main task to fetch deadlines and notify."""
    if moodle is None:
        logger.error("Moodle client not initialized")
        return

    logger.info("Checking for new deadlines...")
    deadlines = moodle.get_upcoming_deadlines()

    if not deadlines:
        logger.info("No deadlines found or error occurred")
        return

    now = datetime.datetime.now().timestamp()
    count = 0
    for deadline in deadlines:
        # Only notify for future deadlines
        if deadline["due_date"] > now:
            if not await is_notified(deadline["id"]):
                due_dt = datetime.datetime.fromtimestamp(
                    deadline["due_date"], tz=ZoneInfo(TIMEZONE)
                )
                formatted_date = due_dt.strftime("%Y-%m-%d %I:%M %p")

                message = (
                    f"🔔 <b>New {deadline['type']} Found!</b>\n\n"
                    f"📌 <b>Title:</b> {deadline['title']}\n"
                    f"📅 <b>Due Date:</b> {formatted_date}\n\n"
                    f"Don't miss it! 🚀"
                )

                await notifier.send_notification(message)
                await mark_as_notified(
                    deadline["id"], deadline["title"], deadline["due_date"]
                )
                count += 1

    logger.info(f"Check complete. Sent {count} new notifications.")


async def main():
    parser = argparse.ArgumentParser(description="Moodle Deadline Notification Bot")
    parser.add_argument(
        "--mock", action="store_true", help="Use mock Moodle client for testing"
    )
    args = parser.parse_args()

    global moodle
    if args.mock:
        logger.info("Using MOCK Moodle client")
        moodle = MockMoodleClient()
    else:
        moodle = MoodleClient()

    # Initialize database
    await init_db()

    # Run immediate check on startup
    await check_for_deadlines()

    # Setup scheduler
    scheduler = AsyncIOScheduler(timezone=TIMEZONE)
    scheduler.add_job(check_for_deadlines, "interval", hours=CHECK_INTERVAL_HOURS)
    scheduler.start()

    logger.info(f"Scheduler started. Checking every {CHECK_INTERVAL_HOURS} hours.")

    # Keep the script running
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
