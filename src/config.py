"""Configuración y constantes del bot."""

import os
from pathlib import Path
from dotenv import load_dotenv


def _get_int_env(var_name: str, default: int) -> int:
	value = os.getenv(var_name)
	if value is None:
		return default
	try:
		return int(value)
	except ValueError:
		return default

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
QWEN_TIMEOUT = _get_int_env("QWEN_TIMEOUT", 300)  # 5 minutos por defecto
