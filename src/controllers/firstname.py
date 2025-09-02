from telegram import Update
from telegram.ext import ContextTypes
from ..helpers.utils import join_args
from ..shared.quota import allow_and_increment
from ..config.settings import Settings
async def firstname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Uso: /firstname Nombre [SegundoNombre]")
        return
    firstnames = join_args(context.args)
    context.user_data["firstname"] = firstnames
    msg = update.effective_message
    await msg.reply_text(
        f"✅ Firstname guardado: {firstnames}\nAhora envía: /lastname Apellido [SegundoApellido]",
        reply_to_message_id=msg.message_id
    )