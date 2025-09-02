# utils/user_id.py
import hmac, hashlib, base64
from ..config.settings import Settings

def make_id15_from_telegram_id(telegram_user_id: int) -> str:
    """
    Genera un ID determinístico de 15 caracteres a partir del telegram_user_id.
    """
    msg = str(telegram_user_id).encode("utf-8")
    key = Settings.SECRET_NAMESPACE.encode("utf-8")
    digest = hmac.new(key, msg, hashlib.sha256).digest()  # 32 bytes
    # Base32 → A-Z2-7 y '=' padding; quitamos '=' y truncamos a 15
    code = base64.b32encode(digest).decode("ascii").rstrip("=")
    return code[:15]
