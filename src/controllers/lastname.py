from telegram import Update
from telegram.ext import ContextTypes

from ..config.settings import Settings
from ..shared.quota import allow_and_increment
from ..helpers.utils import join_args

def _need_firstname_msg() -> str:
    return ("Para buscar a una persona tienes que proporcionar primero un /firstname "
            "seguido de un nombre o dos y luego un /lastname con un apellido o dos. "
            "Recuerda que sin un /firstname no podrás hacer la búsqueda.")



async def lastname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    
    if "firstname" not in context.user_data:
        await update.message.reply_text(_need_firstname_msg())
        return
    if not context.args:
        await update.message.reply_text("Uso: /lastname Apellido [SegundoApellido]")
        return
    lastnames = join_args(context.args)
    context.user_data["lastname"] = lastnames
    msg = update.effective_message
    await msg.reply_text(
        f"✅ Lastname guardado: {lastnames}\nCuando estés listo, envía: /search",
        reply_to_message_id=msg.message_id
    )