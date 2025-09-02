from telegram import Update
from telegram.ext import ContextTypes
from shared.quota import allow_and_increment
from views.response_views import help_text


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(help_text)