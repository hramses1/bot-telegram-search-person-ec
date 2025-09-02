from telegram import Update
from telegram.ext import ContextTypes
from ..views import response_views as views


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(views.init())
    await update.message.reply_text(views.help_text())
    await update.message.reply_text(
        views.disclaimer(),
        parse_mode="Markdown"
    )