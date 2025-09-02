import json
from telegram import Update
from telegram.ext import ContextTypes

from ..services.quota_service import QuotaService

from ..shared.user_id import make_id15_from_telegram_id
from ..lib.api_integration import get_token, search_user
from ..services.reset_service import reset

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.effective_user
    # Recupere los datos del user
    firstname = context.user_data.get("firstname")
    lastname = context.user_data.get("lastname")
    
    # Incrementar cuota
    quota_service = QuotaService(context.user_data)
    allowed, used = quota_service.increment_quota()

    if not allowed:
        await update.message.reply_text("Se te acabaron los mensajes por hoy.")
        return
    

    if not firstname or not lastname:
        await update.message.reply_text("Faltan los datos necesarios: /firstname y /lastname.")
        return
    await update.message.reply_text(f"Buscando a {firstname} {lastname}...")
    id15 = make_id15_from_telegram_id(u.id)
    token = get_token(id15)
    result = search_user(token, firstname, lastname) or []
    
    if result == []:
        await update.message.reply_text("No se encontraron registros.")
    else:
        await update.message.reply_text(f"Resultado de la búsqueda: {len(result)} registro(s) encontrado(s).")

        for i in result:
            result_format = json.dumps(i, indent=4, ensure_ascii=False)
            await update.message.reply_text(f"{result_format}")
        
    await reset(update, context)  # Limpia el contexto después de la búsqueda