from abc import ABC, abstractmethod
from typing import Generator, Tuple

class InterfazMensajeria(ABC):
    """Interfaz abstracta para enviar y recibir mensajes."""
    
    @abstractmethod
    def enviar_mensaje(self, destinatario: str, texto: str) -> None:
        """Envía un mensaje a un destinatario específico."""
        pass

    @abstractmethod
    def escuchar(self) -> Generator[Tuple[str, str], None, None]:
        """Generador que escucha y devuelve mensajes entrantes (remitente, texto)."""
        pass

class InterfazLLM(ABC):
    """Interfaz abstracta para interactuar con un modelo de lenguaje."""
    
    @abstractmethod
    def preguntar(self, prompt: str) -> str:
        """Envía un prompt al modelo y devuelve la respuesta."""
        pass
