import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    PicklePersistence,
)
from src.controllers.reset import reset_quota
from src.services.reset_service import reset
from src.controllers.start import start
from src.controllers.status import status
from src.controllers.firstname import firstname
from src.controllers.lastname import lastname
from src.controllers.search import search
from src.controllers.register_user import register
from src.config.settings import Settings

logging.basicConfig(level=logging.INFO)

def main():
    persistence = PicklePersistence(filepath="estado_bot.pkl")
    app = ApplicationBuilder().token(Settings.BOT_TOKEN).persistence(persistence).build()
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
