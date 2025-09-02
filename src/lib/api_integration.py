import requests
from ..config.settings import Settings

API_URL = Settings.API_BASE_URL
TOKEN = Settings.TOKEN_ENDPOINT
SEARCH = Settings.SEARCH_ENDPOINT
CREATE = Settings.CREATE_ENDPOINT

def get_token(codigo: str) -> str:
    """Obtén un token usando el código de 15 caracteres."""
    response = requests.get(
        f"{API_URL}{TOKEN}",
        params={"codigo": codigo},
        headers={"accept": "application/json"},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("access_token")

def search_user(token: str, firstname: str, lastname: str) -> dict:
    """Busca un usuario usando el token."""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{API_URL}{SEARCH}", params={"name": firstname, "lastname": lastname}, headers=headers
    )
    response.raise_for_status()
    return response.json()

def register_user(payload:dict) -> dict:
    """Registra un nuevo usuario en la API."""
    response = requests.post(f"{API_URL}{CREATE}", json=payload)
    if response.status_code != 200:
        print(response.text)
        return 'Usuario ya registrado'
    return response.json()
