# controllers/admin.py
from datetime import datetime
from zoneinfo import ZoneInfo
from telegram import Update
from telegram.ext import ContextTypes

TZ = ZoneInfo("America/Guayaquil")

async def reset_quota(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Reinicia el contador de mensajes del día para el usuario actual.
    Comando oculto: /resetquota
    """
    today = datetime.now(TZ).date()
    context.user_data["quota"] = {"date": today, "count": 0}
    await update.message.reply_text(
        "🔄 Se reinició tu contador de mensajes para el día de hoy.",
        reply_to_message_id=update.message.message_id
    )
