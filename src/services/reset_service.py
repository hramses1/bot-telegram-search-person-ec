
from telegram import Update
from telegram.ext import ContextTypes

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.pop("firstname", None)
    context.user_data.pop("lastname", None)
    await update.message.reply_text("Se limpió tu contexto. Envía /firstname y /lastname.")