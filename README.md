# Moodle Deadline Notification Bot

A simple Python bot that periodically checks `moodle.mitsgwalior.in` for upcoming assignments and quizzes and sends notifications via Telegram.

## Features
- Fetches deadlines for all enrolled courses.
- Supports both Assignments and Quizzes.
- Prevents duplicate notifications using a local SQLite database.
- Periodically checks for updates using a background scheduler.
- Configurable check interval and timezone.

## Setup Instructions

### 1. Telegram Bot Setup
1. Message [@BotFather](https://t.me/botfather) on Telegram to create a new bot and get your **Bot Token**.
2. Message [@userinfobot](https://t.me/userinfobot) to get your **Chat ID**.

### 2. Local Setup
1. Clone this project to your DigitalOcean droplet.
2. Install `uv` if not already installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. Sync dependencies:
   ```bash
   uv sync
   ```
4. Create a `.env` file in the project root:
   ```env
   MOODLE_URL=https://moodle.mitsgwalior.in
   MOODLE_USERNAME=your_moodle_username
   MOODLE_PASSWORD=your_moodle_password
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   TELEGRAM_CHAT_ID=your_telegram_chat_id
   CHECK_INTERVAL_HOURS=6
   TIMEZONE=Asia/Kolkata
   ```

### 3. Run the Bot
```bash
uv run main.py
```

## Deployment on DigitalOcean (Ubuntu)

1. **Move the project** to `/home/your_user/moodle_bot`.
2. **Update the service file**:
   Edit `moodle_bot.service`:
   - Replace `your_user` with your actual username.
   - Ensure the path to `uv` (`/home/your_user/.cargo/bin/uv`) is correct. You can find it by running `which uv`.
3. **Copy the service file**:
   ```bash
   sudo cp moodle_bot.service /etc/systemd/system/moodle_bot.service
   ```
4. **Start and Enable the service**:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable moodle_bot
   sudo systemctl start moodle_bot
   ```
5. **Check status**:
   ```bash
   sudo systemctl status moodle_bot
   ```

## Note on Moodle API
This bot uses standard Moodle Web Service functions (`mod_assign_get_assignments`, `mod_quiz_get_quizzes_by_courses`). Ensure that your Moodle account has permission to use these web services (usually enabled by default for the mobile app service).
