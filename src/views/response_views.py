import json
from html import escape
from typing import Any, List, Dict

def help_text():
    return (
        "🧭 Cómo buscar personas\n\n"
        "1) Envía primero: /firstname Nombre [SegundoNombre]\n"
        "2) Luego envía: /lastname Apellido [SegundoApellido]\n"
        "3) Finalmente: /search\n\n"
        "📌 Regla: No puedes establecer /lastname si antes no diste un /firstname.\n"
    )
def init():
    return (
        "👋 ¡Bienvenido al bot!\n\n"
        "Aquí tienes las rutas disponibles:\n\n"
        "➡️ /start  – Inicia el bot y muestra este mensaje de ayuda\n"
        "➡️ /register – Regístrate para poder hacer búsquedas\n"
        "➡️ /status – Consulta los valores actuales de /firstname y /lastname\n"
        "➡️ /search – Ejecuta la búsqueda (requiere haberte registrado y haber usado /firstname y /lastname)\n\n"
        "⚡ Próximamente: más comandos que se irán agregando."
    )
def disclaimer():
    """
    Envía un mensaje de advertencia y descargo de responsabilidad sobre el uso de los datos.
    """
    return(
        "⚠️ *Aviso Importante*\n\n"
        "Este bot se conecta a servicios externos para obtener información pública. "
        "Los datos mostrados provienen de fuentes oficiales o abiertas y se entregan "
        "únicamente con fines informativos.\n\n"
        "📌 *Limitaciones y responsabilidad*\n"
        "• No garantizamos que la información presentada sea exacta, completa o esté actualizada al 100%.\n"
        "• El uso que se haga de los datos obtenidos a través de este bot es responsabilidad exclusiva del usuario.\n"
        "• Este bot y sus desarrolladores no se hacen responsables por daños, perjuicios o consecuencias "
        "derivadas de un uso indebido, fraudulento o ilegal de la información.\n\n"
        "🔒 *Privacidad*\n"
        "• No almacenamos información personal sensible más allá de lo necesario para el funcionamiento del bot.\n"
        "• Los registros temporales de búsqueda se utilizan únicamente para mejorar la experiencia de uso y "
        "se eliminan periódicamente.\n\n"
        "Al continuar utilizando este bot, confirmas que comprendes y aceptas estas condiciones."
    )
def quota_info():
    
    return(
        "ℹ️ *Sobre el límite diario de mensajes*\n\n"
        "El contador de mensajes se reinicia automáticamente cada día a la medianoche "
        "según tu zona horaria configurada (por defecto: `America/Guayaquil`).\n\n"
        "Esto significa que:\n"
        "• Si ya usaste todos tus mensajes hoy, tendrás nuevamente el total disponible a partir de las 00:00.\n"
        "• Si consultas `/status` después de medianoche, verás los contadores en cero aunque aún no hayas enviado nada ese día.\n\n"
        "✅ Así garantizamos que siempre tengas un número fijo de mensajes disponibles por día."
    )
def _format_person(p: Dict[str, Any]) -> str:
    return (
        f"<b>Nombre:</b> {escape(str(p.get('Nombre','')))}\n"
        f"<b>Apellido:</b> {escape(str(p.get('Apellido','')))}\n"
        f"<b>CI:</b> <code>{escape(str(p.get('Ci','')))}</code>\n"
        f"<b>Clase:</b> {escape(str(p.get('Clase','')))}\n"
        f"<b>Ciudad:</b> {escape(str(p.get('Ciudad','')))}\n"
        f"<b>Tipo:</b> {escape(str(p.get('TipoIdentificacion','')))}\n"
        f"<b>Dirección:</b> {escape(str(p.get('Direccion','')))}\n"
        f"<b>Fecha Nac.:</b> {escape(str(p.get('FechaNacimiento','')))}\n"
        f"<b>Edad:</b> {escape(str(p.get('Edad','')))}\n"
        f"<b>Género:</b> {escape(str(p.get('Genero','')))}\n"
        f"<b>Nacionalidad:</b> {escape(str(p.get('Nacionalidad','')))}\n"
        f"<b>Estado civil:</b> {escape(str(p.get('EstadoCivil','')))}"
    )
def build_message(results: Any, count: int) -> str:
    if isinstance(results, str):
        try:
            results = json.loads(results)
        except Exception:
            results = []

    results = results or []
    total = len(results)
    n = max(0, min(count, total))

    header = f"🔎 <b>Resultados ({n}/{total})</b>"
    blocks = [header]

    for i, p in enumerate(results[:n], start=1):
        blocks.append(f"\n<b>{i}.</b>\n{_format_person(p)}")

    return "\n".join(blocks)