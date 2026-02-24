import os
import logging
from datetime import time
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TIMEZONE = ZoneInfo(os.getenv("TIMEZONE", "Asia/Tehran"))

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

MEMBERS = "@DrMAminiSh @Telahe72 @kazemi967 @Greeenbear @JahediSaba"

NIGHT_MESSAGE = (
    "عزیزان! برین حیاطتون رو جارو کنین و برگاتون رو جمع کنین! 🍂🍁\n\n"
    + MEMBERS
)

DAY_MESSAGE = (
    "عزیزان! حیاط رو جارو کردین یا برگاتون پخش و پلاست؟ 🍂🍁\n\n"
    + MEMBERS
)


async def send_night_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Send the 12:34 AM reminder."""
    await context.bot.send_message(chat_id=CHAT_ID, text=NIGHT_MESSAGE)
    logger.info("Night reminder sent to chat %s", CHAT_ID)


async def send_day_reminder(context: ContextTypes.DEFAULT_TYPE):
    """Send the 12:34 PM reminder."""
    await context.bot.send_message(chat_id=CHAT_ID, text=DAY_MESSAGE)
    logger.info("Day reminder sent to chat %s", CHAT_ID)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command."""
    await update.message.reply_text(
        "Hello! I'm the Leave Reminder Bot.\n"
        "I'll remind everyone to collect their leaves at 12 AM and 12 PM daily.\n\n"
        "Use /chatid to get this chat's ID for configuration."
    )


async def chatid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /chatid command — prints the current chat's ID."""
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"This chat's ID is: {chat_id}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("chatid", chatid))

    # Schedule reminders only if CHAT_ID is configured
    if CHAT_ID:
        job_queue = app.job_queue
        job_queue.run_daily(send_night_reminder, time=time(hour=0, minute=34, tzinfo=TIMEZONE))
        job_queue.run_daily(send_day_reminder, time=time(hour=12, minute=34, tzinfo=TIMEZONE))
        logger.info("Reminders scheduled for 12:34 AM and 12:34 PM (%s)", TIMEZONE)
    else:
        logger.warning(
            "CHAT_ID not set. Bot will run but no reminders will be sent. "
            "Add the bot to a group, use /chatid, then update .env and restart."
        )

    app.run_polling()


if __name__ == "__main__":
    main()
