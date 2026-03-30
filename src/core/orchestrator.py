from loguru import logger
from src.interfaces.whatsapp import WhatsAppAdapter
from src.interfaces.qwen import QwenAdapter

class BridgeOrchestrator:
    def __init__(self):
        self.wa = WhatsAppAdapter()
        self.qwen = QwenAdapter()

    def run(self):
        """Bucle principal de ejecución."""
        logger.info("Orquestador iniciado. Escuchando mensajes de WhatsApp...")
        
        # Este es un flujo conceptual que debe adaptarse al modo de escucha de wacli
        for incoming in self.wa.listen_messages():
            if incoming is None:
                continue
            
            phone, message = incoming
            logger.info(f"Mensaje recibido de {phone}: {message}")
            
            # 1. Procesar con Qwen
            response = self.qwen.execute_prompt(message)
            
            # 2. Responder por WhatsApp
            self.wa.send_message(phone, response)
