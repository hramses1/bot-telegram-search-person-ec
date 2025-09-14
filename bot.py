import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    PicklePersistence,
)

from src.controllers.reset import reset_quota          # /reset_quota (oculto)
from src.services.reset_service import reset           # /reset
from src.controllers.start import start                # /start
from src.controllers.status import status              # /status
from src.controllers.firstname import firstname        # /firstname
from src.controllers.lastname import lastname          # /lastname
from src.controllers.search import search              # /search
from src.controllers.register_user import register     # /register
from src.config.settings import Settings

# ────────────────────────────────────────────────────────────
# Logging (menos ruido de PTB en consola)
# ────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.WARNING, format="%(levelname)s:%(name)s:%(message)s")
log = logging.getLogger("bot")
logging.getLogger("telegram").setLevel(logging.ERROR)
logging.getLogger("telegram.ext").setLevel(logging.ERROR)

# ────────────────────────────────────────────────────────────
# ────────────────────────────────────────────────────────────
# Cierre ordenado (si usas httpx.AsyncClient en tu API)
# ────────────────────────────────────────────────────────────
async def on_shutdown(app):
    try:
        # Cierra el cliente HTTP asíncrono si lo usas
        from src.lib import api_integration_async as api  # opcional
        await api.client.aclose()
    except Exception:
        pass

def main():
    persistence = PicklePersistence(filepath="estado_bot.pkl")

    app = (
        ApplicationBuilder()
        .token(Settings.BOT_TOKEN)
        .persistence(persistence)
        .concurrent_updates(True)
        .post_shutdown(on_shutdown)
        .build()
    )

    # Handlers de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("firstname", firstname))
    app.add_handler(CommandHandler("lastname", lastname))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("reset_quota", reset_quota))

    app.run_polling()

if __name__ == "__main__":
    main()
