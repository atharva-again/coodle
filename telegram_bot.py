import logging

from telegram import Bot
from telegram.constants import ParseMode

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self):
        if not TELEGRAM_BOT_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN is not set")
            # We don't want to crash here, but bot will be None
            self.bot = None
        else:
            self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.chat_id = TELEGRAM_CHAT_ID

    async def send_notification(self, message: str) -> bool:
        """Send a message to the configured Telegram chat."""
        if not self.bot:
            logger.error("Telegram bot not initialized")
            return False
        if not self.chat_id:
            logger.error("TELEGRAM_CHAT_ID not configured")
            return False

        try:
            # Increase read_timeout to handle slow connections
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode=ParseMode.HTML,
                read_timeout=30,
            )
            logger.info("Telegram notification sent")
            return True
        except Exception as e:
            logger.error(f"Error sending Telegram notification: {e}")
            return False
