# src/controllers/search.py
import io
import json
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ..views.response_views import build_message

from ..helpers.utils import quota_remaining_today,cleaner_data

from ..services.quota_service import QuotaService
from ..shared.user_id import make_id15_from_telegram_id
from ..lib.api_integration import get_token, search_user  # <- tus funciones síncronas (requests)
from ..services.reset_service import reset
from ..lib.threadpool import EXECUTOR

MAX_INLINE_CHARS = 3500
TOP_N = 10

def _make_preview(results: list[dict]) -> str:
    if not results:
        return "No se encontraron resultados."
    header = f"🔎 Resultados encontrados: {len(results)}\n\n"
    return header
def _make_doc(results: list[dict], firstname , lastname,):
    try:
        data_bytes = json.dumps(results, ensure_ascii=False, indent=2).encode("utf-8")
        bio = io.BytesIO(data_bytes); bio.name = f"resultados_{firstname}_{lastname}.json"
    except Exception:
        pass
    return bio
def _chunk_text(text: str, limit: int = 3900):
    for i in range(0, len(text), limit):
        yield text[i:i+limit]

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    user = update.effective_user

    # 1) Cuota (esto sí consume)
    quota = QuotaService(context.user_data)
    allowed, _ = quota.increment_quota()
    if not allowed:
        await msg.reply_text("Se te acabaron los mensajes por hoy.", reply_to_message_id=msg.message_id)
        return

    # 2) Datos
    firstname = cleaner_data(context.user_data.get("firstname"))
    lastname  = cleaner_data(context.user_data.get("lastname"))
    if not firstname or not lastname:
        await msg.reply_text("Faltan los datos necesarios: /firstname y /lastname.", reply_to_message_id=msg.message_id)
        return

    # 3) Aviso inmediato (UX) y capturar valores para el hilo
    await msg.reply_text(f"Buscando a {firstname} {lastname}…", reply_to_message_id=msg.message_id)
    id15 = make_id15_from_telegram_id(user.id)

    loop = asyncio.get_running_loop()

    # 4) Trabajo bloqueante (requests) en hilo
    def work_blocking(id15_local: str, fn: str, ln: str):
        # ⚠️ NO LLAMES Telegram API AQUÍ DENTRO
        token = get_token(id15_local)
        context.user_data["token"] = token
        results = search_user(token, fn, ln) or []
        return results

    try:
        results = await loop.run_in_executor(EXECUTOR, work_blocking, id15, firstname, lastname)
    except Exception as e:
        await msg.reply_text(f"⚠️ No se pudo completar la búsqueda. Intenta más tarde.", reply_to_message_id=msg.message_id)
        return
    remaining = quota_remaining_today(context.user_data)
    # 5) Responder (de vuelta en el event loop)
    if not results:
        await msg.reply_text("No se encontraron registros.", reply_to_message_id=msg.message_id)
        await reset(update, context)
        await msg.reply_text(f"Te quedan {remaining} mensajes hoy.", reply_to_message_id=msg.message_id)
        return

    count_result = len(results)
    
    if count_result < 5:
    # Preview seguro
        await msg.reply_text(_make_preview(results), reply_to_message_id=msg.message_id)
        text = build_message(results, count_result)
        for chunk in _chunk_text(text):
            await msg.reply_text(
                chunk,
                reply_to_message_id=msg.message_id,
                parse_mode=ParseMode.HTML
            )
    else:
        await msg.reply_text(_make_preview(results), reply_to_message_id=msg.message_id)
        await msg.reply_document(document=_make_doc(results,firstname,lastname), caption="📎 Resultados completos (JSON)")

    await reset(update, context)
    await msg.reply_text(f"✅ Búsqueda completada. Te quedan {remaining} mensajes hoy.", reply_to_message_id=msg.message_id)
