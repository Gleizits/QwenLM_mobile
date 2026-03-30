import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Ajustes(BaseSettings):
    """Configuración simple de la aplicación."""
    qwen_path: str = os.getenv("QWEN_PATH", "qwen")
    telefono_defecto: str = os.getenv("DEFAULT_PHONE", "")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Ajustes()
