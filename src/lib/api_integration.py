import requests
from requests.exceptions import RequestException, HTTPError, Timeout
from ..config.settings import Settings

API_URL = Settings.API_BASE_URL
TOKEN = Settings.TOKEN_ENDPOINT
SEARCH = Settings.SEARCH_ENDPOINT
CREATE = Settings.CREATE_ENDPOINT
GET_PLANS = Settings.GET_PLANS_ENDPOINT

DEFAULT_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

TIMEOUT = 1000  # segundos

class ApiError(Exception):
    """Error genérico de API."""
    pass


def get_token(codigo: str) -> str:
    """Obtén un token usando el código de 15 caracteres."""
    try:
        resp = requests.get(
            f"{API_URL}{TOKEN}",
            params={"codigo": codigo},
            headers=DEFAULT_HEADERS,
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()
        token = data.get("access_token")
        if not token:
            raise ApiError(f"La API no devolvió access_token. Respuesta: {data}")
        return token
    except (HTTPError, Timeout, RequestException) as e:
        raise ApiError(f"Error al obtener token: {e}")

def get_plans_for_userId(userid:str) -> dict:
    """ Obtén los planes asociados a un userId """
    try:
        resp = requests.get(
            f"{API_URL}{GET_PLANS}",
            params={"userid": userid},
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()
    except (HTTPError, Timeout, RequestException) as e:
        raise ApiError(f"Error en búsqueda: {e}")
    
def update_user(userid:str,json: dict) -> dict:
    """ Actualiza los datos de un usuario dado su userId """
    try:
        resp = requests.get(
            f"{API_URL}{GET_PLANS}",
            params={"userid": userid},
            json=json,
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()
    except (HTTPError, Timeout, RequestException) as e:
        raise ApiError(f"Error en búsqueda: {e}")



def search_user(token: str, firstname: str, lastname: str) -> dict:
    """Busca un usuario usando el token válido."""
    headers = {**DEFAULT_HEADERS, "Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(
            f"{API_URL}{SEARCH}",
            params={"name": firstname, "lastname": lastname},
            headers=headers,
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
        return resp.json()
    except (HTTPError, Timeout, RequestException) as e:
        raise ApiError(f"Error en búsqueda: {e}")


def register_user(payload: dict) -> dict:
    """Registra un nuevo usuario en la API."""
    try:
        resp = requests.post(
            f"{API_URL}{CREATE}",
            json=payload,
            headers=DEFAULT_HEADERS,
            timeout=TIMEOUT,
        )
        if resp.status_code == 500:
            # conflicto típico → ya existe
            return {"error": "Usuario ya registrado"}
        resp.raise_for_status()
        return resp.json()
    except (HTTPError, Timeout, RequestException) as e:
        raise ApiError(f"Error en registro: {e}")
