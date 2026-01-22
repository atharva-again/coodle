import logging
from telegram import Bot
from telegram.constants import ParseMode
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.chat_id = TELEGRAM_CHAT_ID

    async def send_notification(self, message: str):
        """Send a message to the configured Telegram chat."""
        if not self.chat_id:
            logger.error("TELEGRAM_CHAT_ID not configured")
            return

        try:
            await self.bot.send_message(
                chat_id=self.chat_id, text=message, parse_mode=ParseMode.HTML
            )
            logger.info("Telegram notification sent")
        except Exception as e:
            logger.error(f"Error sending Telegram notification: {e}")
