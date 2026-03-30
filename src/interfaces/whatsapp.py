import subprocess
import shlex
from loguru import logger
from src.config import settings

class WhatsAppAdapter:
    def __init__(self, binary_path: str = settings.wacli_path):
        self.binary_path = binary_path

    def send_message(self, phone: str, message: str):
        """Envía un mensaje a través de wacli."""
        try:
            # Ejemplo: wacli send --to 123456789 "mensaje"
            # Ajustar según la sintaxis real de wacli
            cmd = [self.binary_path, "send", "--to", phone, message]
            subprocess.run(cmd, check=True)
            logger.info(f"Mensaje enviado a {phone}")
        except Exception as e:
            logger.error(f"Error enviando mensaje por WhatsApp: {e}")

    def listen_messages(self):
        """
        Escucha mensajes entrantes. 
        Nota: Esto dependerá de si wacli ofrece un modo 'stream' o similar.
        """
        # Por ahora, un placeholder. wacli suele requerir un daemon o polling.
        logger.warning("listen_messages no implementado aún. Requiere definir el modo de escucha de wacli.")
        yield None
