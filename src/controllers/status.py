from telegram import Update
from telegram.ext import ContextTypes

from ..lib.api_integration import get_plans_for_userId

from ..views.response_views import quota_info

from ..helpers.utils import quota_remaining_today, quota_used_today
from ..config.settings import Settings

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Muestra el estado actual del usuario sin consumir cuota."""
    limit_per_day = get_plans_for_userId(context.user_data.get("userid"))
    max_msgs = limit_per_day['items'][0]['token_duration']

    used = quota_used_today(context.user_data)
    remaining = quota_remaining_today(context.user_data)

    fn = context.user_data.get("firstname", "—")
    ln = context.user_data.get("lastname", "—")

    msg = (
        "📊 *Estado actual*\n"
        f"• Firstname: `{fn}`\n"
        f"• Lastname: `{ln}`\n"
        f"• Usados hoy: {used}\n"
        f"• Restantes: {remaining} (límite: {max_msgs})"
    )

    await update.message.reply_text(
        msg, parse_mode="Markdown", 
        reply_to_message_id=update.message.message_id
        )
    
    await update.message.reply_text(
        quota_info(), parse_mode="Markdown", 
        reply_to_message_id=update.message.message_id
        )