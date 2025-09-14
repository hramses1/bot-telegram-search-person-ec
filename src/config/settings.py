import os
from dataclasses import dataclass
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

load_dotenv()

@dataclass(frozen=True)
class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    TZ: str = ZoneInfo(os.getenv("TZ", "America/Guayaquil"))
    MAX_MSGS: int = int(os.getenv("MAX_MSGS", "20"))

    API_BASE_URL: str = os.getenv("API_BASE_URL", "").rstrip("/")
    CREATE_ENDPOINT: str = os.getenv("CREATE_ENDPOINT",)
    TOKEN_ENDPOINT: str = os.getenv("TOKEN_ENDPOINT")
    SEARCH_ENDPOINT: str = os.getenv("SEARCH_ENDPOINT",)
    GET_PLANS_ENDPOINT: str = os.getenv("GET_PLANS_ENDPOINT",)
    API_USERNAME: str = os.getenv("API_USERNAME", "")
    API_PASSWORD: str = os.getenv("API_PASSWORD", "")
    AUTH_CACHE_SECONDS: int = int(os.getenv("AUTH_CACHE_SECONDS", "3300"))  # ~55min
    SECRET_NAMESPACE : str = os.getenv("SECRET_NAMESPACE", "tu-secreto-super-estable")

settings = Settings()
