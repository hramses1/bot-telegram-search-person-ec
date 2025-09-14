from datetime import datetime, timezone

from ..lib.api_integration import get_plans_for_userId, update_user
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
            
        limit_per_day = get_plans_for_userId(self.user.get('userid'))

        # Si ya alcanzó el límite, no permitir
        if quota["count"] >= limit_per_day['items'][0]['token_duration']:
            self.user["quota"] = quota
            return False, quota["count"]

        # Incrementar y permitir
        quota["count"] += 1
        self.user["quota"] = quota
        update_user(self.user.get('userid'), {"number_requests": self.user.get('number_requests', 0) + 1})
        return True, quota["count"]
