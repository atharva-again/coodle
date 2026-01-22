import os

from dotenv import load_dotenv

load_dotenv()

# Moodle Settings
MOODLE_URL = os.getenv("MOODLE_URL", "https://moodle.mitsgwalior.in")
MOODLE_USERNAME = os.getenv("MOODLE_USERNAME")
MOODLE_PASSWORD = os.getenv("MOODLE_PASSWORD")

# Telegram Settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# App Settings
CHECK_INTERVAL_HOURS = int(os.getenv("CHECK_INTERVAL_HOURS", "6"))
DATABASE_PATH = os.getenv("DATABASE_PATH", "moodle_bot.db")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Kolkata")
