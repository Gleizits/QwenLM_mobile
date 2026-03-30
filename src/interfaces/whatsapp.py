import time
from typing import Generator, Tuple
from neonize.client import NewClient
from neonize.events import MessageEv, ConnectedEv, QREv
from src.interfaces.base import InterfazMensajeria
from src.utils.exceptions import console

class AdaptadorWhatsApp(InterfazMensajeria):
    """Adaptador nativo de WhatsApp con Neonize (API actualizada)."""
    
    def __init__(self, db_name: str = "whatsapp_session.db"):
        self.client = NewClient(db_name)
        self.mensajes_pendientes = []
        
        # Registro de eventos como decoradores
        @self.client.event(ConnectedEv)
        def al_conectar(_, __):
            console.print("[bold green]✔ WhatsApp conectado correctamente.[/bold green]")

        @self.client.event(QREv)
        def al_recibir_qr(_, qr_content: str):
            console.print("[bold yellow]Escanea el código QR en la terminal para iniciar sesión.[/bold yellow]")

        @self.client.event(MessageEv)
        def al_recibir_mensaje(_, message: MessageEv):
            try:
                # Intento de detección robusta del remitente y el contenido
                # En algunas versiones neonize usa camelCase (isFromMe) o snake_case (is_from_me)
                info = message.Info
                
                # Intentamos detectar si es propio (para ignorar sincronizaciones)
                es_mio = getattr(info, "IsFromMe", getattr(info, "isFromMe", False))
                if es_mio:
                    return

                # Remitente
                remitente_obj = getattr(info, "Sender", None)
                remitente = remitente_obj.String() if remitente_obj else "desconocido"
                
                # Contenido del texto
                msg_content = message.Message
                texto = ""
                
                if hasattr(msg_content, "conversation") and msg_content.conversation:
                    texto = msg_content.conversation
                elif hasattr(msg_content, "extendedTextMessage") and msg_content.extendedTextMessage.text:
                    texto = msg_content.extendedTextMessage.text
                
                if texto:
                    self.mensajes_pendientes.append((remitente, texto))
                    
            except Exception as e:
                # Silenciamos errores de parsing de mensajes de sistema (como sincronización)
                pass

    def enviar_mensaje(self, destinatario: str, texto: str) -> None:
        try:
            self.client.send_message(destinatario, texto)
            console.print(f"[bold green]✔ Respuesta enviada a {destinatario}[/bold green]")
        except Exception as e:
            console.print(f"[bold red]❌ Error al enviar mensaje:[/bold red] {e}")

    def escuchar(self) -> Generator[Tuple[str, str], None, None]:
        console.print("[bold cyan]Conectando con WhatsApp...[/bold cyan]")
        self.client.connect()
        console.print("[italic green]Esperando mensajes... (Ctrl+C para salir)[/italic green]")
        
        try:
            while True:
                if self.mensajes_pendientes:
                    yield self.mensajes_pendientes.pop(0)
                time.sleep(0.5)
        except KeyboardInterrupt:
            console.print("\n[bold red]Desconectando WhatsApp...[/bold red]")
            self.client.disconnect()
