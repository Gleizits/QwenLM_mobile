"""Configuración y constantes del bot."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Discord
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")

# Seguridad
ADMIN_USER_ID = os.getenv("ADMIN_USER_ID")
WHITELIST_FILE = DATA_DIR / "whitelist.json"
COMMAND_HISTORY_FILE = DATA_DIR / "command_history.json"

# Qwen Code
QWEN_COMMAND = os.getenv("QWEN_COMMAND", "qwen")
QWEN_TIMEOUT = int(os.getenv("QWEN_TIMEOUT", "300"))  # 5 minutos por defecto
