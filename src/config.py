import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    wacli_path: str = os.getenv("WACLI_PATH", "wacli")
    qwen_path: str = os.getenv("QWEN_PATH", "qwen")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
