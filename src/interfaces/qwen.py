import subprocess
import shlex
from loguru import logger
from src.config import settings

class QwenAdapter:
    def __init__(self, binary_path: str = settings.qwen_path):
        self.binary_path = binary_path

    def execute_prompt(self, prompt: str) -> str:
        """Ejecuta un prompt en Qwen CLI y devuelve la respuesta."""
        try:
            logger.debug(f"Ejecutando Qwen con prompt: {prompt}")
            # Ejemplo: qwen-cli "mi prompt"
            # Ajustar según la sintaxis real de qwen-cli (npm)
            result = subprocess.run(
                [self.binary_path, prompt],
                capture_output=True,
                text=True,
                encoding='utf-8',
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f"Error ejecutando Qwen: {e.stderr}")
            return f"Error: {e.stderr}"
        except Exception as e:
            logger.error(f"Error inesperado en QwenAdapter: {e}")
            return str(e)
