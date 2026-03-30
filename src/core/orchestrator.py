from rich.panel import Panel
from src.interfaces.base import InterfazMensajeria, InterfazLLM
from src.utils.exceptions import console

class OrquestadorPuente:
    """Lógica simplificada con interfaz de usuario amigable."""
    
    def __init__(self, mensajeria: InterfazMensajeria, llm: InterfazLLM):
        self.mensajeria = mensajeria
        self.llm = llm

    def ejecutar(self) -> None:
        console.print(Panel.fit(
            "QWEN MOBILE BRIDGE", 
            style="bold cyan", 
            subtitle="v1.0"
        ))
        
        try:
            for remitente, mensaje in self.mensajeria.escuchar():
                # 1. Procesar con Qwen
                respuesta = self.llm.preguntar(mensaje)
                
                # Mostrar respuesta en consola para el usuario local
                console.print(Panel(respuesta, title="[bold cyan]Qwen Responde[/bold cyan]", border_style="cyan"))
                
                # 2. Enviar por WhatsApp
                self.mensajeria.enviar_mensaje(remitente, respuesta)
        
        except KeyboardInterrupt:
            console.print("\n[bold red]Saliendo...[/bold red]")
