# controllers/register_user.py
import asyncio
from telegram import Update
from telegram.ext import ContextTypes

from ..shared.user_id import make_id15_from_telegram_id
from ..services.quota_service import QuotaService
from ..views import response_views as views
from ..config.settings import Settings
from ..lib.api_integration import get_plans_for_userId, register_user
from ..schemas.user_schema import AccountPlan, UserSchema, handle_register_user
from ..lib.threadpool import EXECUTOR

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    u = update.effective_user
    msg_id = msg.message_id
    limit_per_day = get_plans_for_userId(make_id15_from_telegram_id(u.id))
    context.user_data["userid"] = make_id15_from_telegram_id(u.id)

    # 0) Mostrar feedback inmediato (no bloqueante)
    await msg.reply_text("Registrando tu cuenta…", reply_to_message_id=msg_id)

    # 1) Preparar payload (todo fuera del hilo)
    id15 = make_id15_from_telegram_id(u.id)
    payload = UserSchema(
        id=str(id15),
        username=u.username or "sinusername",
        email=f"{u.id}@devnull.com",
        emailVisibility=True,
        disabled=False,
        number_requests=0,
        plan=AccountPlan.FREE,
        name=f"{(u.first_name or 'test')} {(u.last_name or 'test')}" or None,
        token="token_initial",
    ).dict()

    # 2) Trabajo bloqueante en hilo
    loop = asyncio.get_running_loop()

    def work_blocking(p: dict):
        # ⚠️ SOLO I/O con requests aquí; no uses objetos de Telegram dentro del hilo
        return register_user(p)

    try:
        result = await loop.run_in_executor(EXECUTOR, work_blocking, payload)
    except Exception as e:
        await msg.reply_text(
            f"⚠️ No se pudo completar el registro. Intenta más tarde.",
            reply_to_message_id=msg_id
        )
        return

    # 3) Validar respuesta de la API y responder
    valid_result = handle_register_user(result)

    await msg.reply_text(valid_result, reply_to_message_id=msg_id)
    
    # 4) Mostrar estado de cuota (sin consumir)
    qs = QuotaService(context.user_data)  # asume que tiene remaining_today()
    remaining = qs.remaining_today() if hasattr(qs, "remaining_today") else limit_per_day['items'][0]['token_duration']
    await msg.reply_text(
        f"Te quedan {remaining} mensajes hoy (límite: {limit_per_day['items'][0]['token_duration']}).",
        reply_to_message_id=msg_id
    )

    # 5) Ayuda/Comandos
    await msg.reply_text(views.help_text(), reply_to_message_id=msg_id)
