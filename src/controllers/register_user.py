from telegram import Update
from telegram.ext import ContextTypes

from ..shared.user_id import make_id15_from_telegram_id
from ..services.quota_service import QuotaService
from ..views import response_views as views
from ..config.settings import Settings
from ..lib.api_integration import register_user
from ..schemas.user_schema import AccountPlan, UserSchema, handle_register_user

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):

    u = update.effective_user 
    id15 = make_id15_from_telegram_id(u.id)
    
    payload = UserSchema(
    id=str(id15),
    username=u.username or "sinusername",
    email=f"{u.id}@devnull.com",
    emailVisibility=True,
    disabled=False,
    number_requests=0,
    plan=AccountPlan.FREE,
    name=f"{u.first_name or ''} {u.last_name or ''}".strip() or None,
    token="token_initial",
    )
    result = register_user(payload.dict())
    
    valid_result = handle_register_user(result)

    await update.message.reply_text(valid_result)

    await update.message.reply_text(f"Tienes {Settings.MAX_MSGS} mensajes por hoy.")
    await update.message.reply_text(views.help_text())
