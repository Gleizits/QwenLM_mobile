"""Configuración y constantes del bot."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def _get_int_env(var_name: str, default: int) -> int:
    """Obtiene una variable de entorno como entero con valor por defecto."""
    try:
        return int(os.environ[var_name])
    except (KeyError, ValueError):
        return default


# Paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Discord
DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
DISCORD_CLIENT_ID: str = os.getenv("DISCORD_CLIENT_ID", "")

# Seguridad
ADMIN_USER_ID: str = os.getenv("ADMIN_USER_ID", "")
WHITELIST_FILE: Path = DATA_DIR / "whitelist.json"
COMMAND_HISTORY_FILE: Path = DATA_DIR / "command_history.json"

# Qwen Code
QWEN_COMMAND: str = os.getenv("QWEN_COMMAND", "qwen")
QWEN_TIMEOUT: int = _get_int_env("QWEN_TIMEOUT", 300)