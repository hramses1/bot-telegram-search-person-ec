from datetime import datetime, timezone
from ..config.settings import Settings

class QuotaService:
    def __init__(self, user):
        self.user = user

    def increment_quota(self):
        today = datetime.now(Settings.TZ).date()
        
        print("User before quota check:", self.user)  # Debug print 
        quota = self.user.get("quota", {"date": today, "count": 0})

        # Reset si cambió el día
        if quota["date"] != today:
            quota = {"date": today, "count": 0}

        # Si ya alcanzó el límite, no permitir
        if quota["count"] >= Settings.MAX_MSGS:
            self.user["quota"] = quota
            return False, quota["count"]

        # Incrementar y permitir
        quota["count"] += 1
        self.user["quota"] = quota
        return True, quota["count"]
