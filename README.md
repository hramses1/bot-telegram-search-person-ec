# Telegram Search Bot

Bot de Telegram para búsquedas con control de cuota diaria, registro de usuario y comandos utilitarios.

---

## ✨ Características
- Registro y login contra API externa.
- Búsqueda por `/firstname` + `/lastname` y ejecución con `/search`.
- Límite de mensajes por día (configurable).
- ID determinístico de 15 caracteres por usuario (HMAC + Base32).
- Comando oculto de administración para reiniciar la cuota.
- Mensajes en hilo (responde directamente al mensaje del usuario).
- Aviso de uso de datos (disclaimer).

---

## 📦 Requisitos
- Python **3.11+**
- Cuenta de bot de Telegram (creada con [@BotFather](https://t.me/BotFather))
- Variables de entorno configuradas en `.env`

---

## ⚙️ Instalación y configuración

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/<tu-usuario>/<tu-repo>.git
   cd <tu-repo>
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Linux/Mac
   source .venv/bin/activate
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Crear archivo `.env` a partir de `.env.example` y rellenar:
   ```env
   BOT_TOKEN=tu_token_de_telegram
   MAX_MSGS=20
   SECRET_NAMESPACE=tu-secreto-super-estable
   API_URL=api
   TZ=America/Guayaquil
   ```

---

## ▶️ Ejecución

```bash
python bot.py
```

---

## 📖 Comandos disponibles

- `/start` – Inicia el bot, muestra ayuda y el aviso de uso de datos.  
- `/register` – Regístrate para poder hacer búsquedas.  
- `/firstname <nombres>` – Guarda uno o dos nombres.  
- `/lastname <apellidos>` – Guarda uno o dos apellidos.  
- `/search` – Ejecuta la búsqueda (requiere registro y firstname/lastname).  
- `/status` – Muestra los valores actuales de `/firstname` y `/lastname`, además de la cuota diaria.  
- `/reset` – Limpia tu contexto (`firstname` y `lastname`).  
- `/disclaimer` – Muestra aviso y descargo de responsabilidad sobre el uso de datos.  
- `/resetquota` – 🔒 (Comando oculto/Admin) Reinicia la cuota de mensajes del día.  

---

## 🧑‍💻 Estándares de contribución

- **Commits**: estilo [Conventional Commits](https://www.conventionalcommits.org/)  
  Ejemplo: `feat: add /resetquota command`  
- **Versionado**: [SemVer](https://semver.org/lang/es/) (ej. `v0.1.0`)  
- **Changelog**: se mantiene en `CHANGELOG.md`

---

## 🔒 Seguridad

- Nunca subas tu `.env` al repositorio.  
- Para reportar vulnerabilidades, revisa el archivo `SECURITY.md`.  

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.
