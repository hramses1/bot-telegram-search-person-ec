from datetime import datetime
from ..config.settings import Settings

def join_args(parts):
    return " ".join(parts).strip()

def check_firstname(context):
    return "firstname" not in context.user_data

def _reset_if_new_day(user_data: dict) -> dict:
    today = datetime.now(Settings.TZ).date()
    quota = user_data.get("quota", {"date": today, "count": 0})
    if quota["date"] != today:
        quota = {"date": today, "count": 0}
        user_data["quota"] = quota
    return quota

def quota_used_today(user_data: dict) -> int:
    """Devuelve usados hoy SIN incrementar."""
    quota = _reset_if_new_day(user_data)
    return int(quota.get("count", 0))

def quota_remaining_today(user_data: dict) -> int:
    """Devuelve restantes hoy SIN incrementar."""
    used = quota_used_today(user_data)
    return max(0, Settings.MAX_MSGS - used)