from datetime import datetime, date, timezone
from zoneinfo import ZoneInfo
from typing import Tuple, Dict

def allow_and_increment(user_data: Dict, max_msgs: int, tz_name: str) -> Tuple[bool, int]:
    """Devuelve (permitido, usados_tras_incremento_o_actuales)."""
    tz = tz_name
    today: date = datetime.now(tz).date()
    quota = user_data.get("quota", {"date": today, "count": 0})

    # reset diario
    if quota["date"] != today:
        quota = {"date": today, "count": 0}

    if quota["count"] >= max_msgs:
        user_data["quota"] = quota
        return False, quota["count"]

    quota["count"] += 1
    user_data["quota"] = quota
    return True, quota["count"]
