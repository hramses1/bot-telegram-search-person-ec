# Bot de Telegram: /firstname, /lastname, /search con límite diario y limpieza post-búsqueda
# python-telegram-bot v20+

import os
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

from typing import List, Tuple

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    PicklePersistence,
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("search-bot")

# ---- LÍMITE DIARIO ----
MAX_MSGS = 20
TZ = ZoneInfo("America/Guayaquil")

def _allow_and_increment(user_data: dict) -> Tuple[bool, int]:
    """Devuelve (permitido, usados_tras_incremento_o_actuales)."""
    today = datetime.now(TZ).date()
    quota = user_data.get("quota", {"date": today, "count": 0})

    # Reset si cambió el día
    if quota["date"] != today:
        quota = {"date": today, "count": 0}

    # Si ya alcanzó el límite, no permitir
    if quota["count"] >= MAX_MSGS:
        user_data["quota"] = quota
        return False, quota["count"]

    # Incrementar y permitir
    quota["count"] += 1
    user_data["quota"] = quota
    return True, quota["count"]

# ---- AYUDA ----
HELP_TEXT = (
    "🧭 Cómo buscar personas\n\n"
    "1) Envía primero: /firstname Nombre [SegundoNombre]\n"
    "2) Luego envía: /lastname Apellido [SegundoApellido]\n"
    "3) Finalmente: /search\n\n"
    "📌 Regla: No puedes establecer /lastname si antes no diste un /firstname.\n"
    "Ejemplos:\n"
    "• /firstname Hector Jose\n"
    "• /lastname Arismendi Asqui\n"
    "• /search\n"
)

def _join(parts: List[str]) -> str:
    return " ".join(parts).strip()

def _need_firstname_msg() -> str:
    return ("Para buscar a una persona tienes que proporcionar primero un /firstname "
            "seguido de un nombre o dos y luego un /lastname con un apellido o dos. "
            "Recuerda que sin un /firstname no podrás hacer la búsqueda.")

# ---- HANDLERS (con límite aplicado) ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    allowed, used = _allow_and_increment(context.user_data)
    if not allowed:
        await update.message.reply_text("Se te acabaron los mensajes por hoy.")
        return
    
    await update.message.reply_text(f"Tienes {MAX_MSGS} mensajes por hoy.")
    await update.message.reply_text(HELP_TEXT)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    allowed, used = _allow_and_increment(context.user_data)
    if not allowed:
        await update.message.reply_text("Se te acabaron los mensajes por hoy.")
        return
    await update.message.reply_text(HELP_TEXT)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    allowed, used = _allow_and_increment(context.user_data)
    if not allowed:
        await update.message.reply_text("Se te acabaron los mensajes por hoy.")
        return
    context.user_data.pop("firstname", None)
    context.user_data.pop("lastname", None)
    await update.message.reply_text("Se limpió tu contexto. Envía /firstname y /lastname.")

async def firstname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    allowed, used = _allow_and_increment(context.user_data)
    if not allowed:
        await update.message.reply_text("Se te acabaron los mensajes por hoy.")
        return

    if not context.args:
        await update.message.reply_text("Uso: /firstname Nombre [SegundoNombre]")
        return
    firstnames = _join(context.args)
    context.user_data["firstname"] = firstnames
    await update.message.reply_text(f"✅ Firstname guardado: {firstnames}\nAhora envía: /lastname Apellido [SegundoApellido]")

async def lastname(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    allowed, used = _allow_and_increment(context.user_data)
    if not allowed:
        await update.message.reply_text("Se te acabaron los mensajes por hoy.")
        return

    if "firstname" not in context.user_data:
        await update.message.reply_text(_need_firstname_msg())
        return
    if not context.args:
        await update.message.reply_text("Uso: /lastname Apellido [SegundoApellido]")
        return
    lastnames = _join(context.args)
    context.user_data["lastname"] = lastnames
    await update.message.reply_text(f"✅ Lastname guardado: {lastnames}\nCuando estés listo, envía: /search")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    allowed, used = _allow_and_increment(context.user_data)
    if not allowed:
        await update.message.reply_text("Se te acabaron los mensajes por hoy.")
        return

    firstnames = context.user_data.get("firstname")
    lastnames = context.user_data.get("lastname")

    if not firstnames:
        await update.message.reply_text(_need_firstname_msg())
        return
    if not lastnames:
        await update.message.reply_text("Aún no has enviado /lastname. Ejemplo: /lastname Perez Gomez")
        return

    query = f"{firstnames} {lastnames}"
    # TODO: aquí implementa tu lógica real de búsqueda
    await update.message.reply_text(f"🔎 Buscando: {query}\n(Implementa aquí tu lógica de búsqueda)")

    # 🔥 limpiar historial después de buscar y mostrar mensajes restantes
    context.user_data.pop("firstname", None)
    context.user_data.pop("lastname", None)
    remaining = max(0, MAX_MSGS - used)
    await update.message.reply_text(
        f"✅ Historial limpiado. Te quedan {remaining} mensajes hoy.\n"
        "Puedes iniciar una nueva búsqueda con /firstname y /lastname."
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    allowed, used = _allow_and_increment(context.user_data)
    if not allowed:
        await update.message.reply_text("Se te acabaron los mensajes por hoy.")
        return
    fn = context.user_data.get("firstname", "—")
    ln = context.user_data.get("lastname", "—")
    remaining = max(0, MAX_MSGS - used)
    await update.message.reply_text(f"Estado actual:\n• Firstname: {fn}\n• Lastname: {ln}\n• Te quedan {remaining} mensajes hoy.")

def main() -> None:
    persistence = PicklePersistence(filepath="estado_bot.pkl")
    app = ApplicationBuilder().token(TOKEN).persistence(persistence).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("firstname", firstname))
    app.add_handler(CommandHandler("lastname", lastname))
    app.add_handler(CommandHandler("search", search))

    app.run_polling()

if __name__ == "__main__":
    main()
