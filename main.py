import typer
from src.config import settings
from src.core.orchestrator import OrquestadorPuente
from src.interfaces.whatsapp import AdaptadorWhatsApp
from src.interfaces.qwen import AdaptadorQwen

# Inicializar CLI de Typer
app = typer.Typer(add_completion=False)

@app.command()
def iniciar():
    """Inicia el puente móvil para Qwen."""
    try:
        # Inicialización de adaptadores con los nombres de argumentos correctos
        wa_adapter = AdaptadorWhatsApp()  # Neonize usa whatsapp_session.db por defecto
        qwen_adapter = AdaptadorQwen(binary_name=settings.qwen_path)
        
        # Iniciar orquestador
        orquestador = OrquestadorPuente(
            mensajeria=wa_adapter,
            llm=qwen_adapter
        )
        
        orquestador.ejecutar()
        
    except Exception as e:
        print(f"Error fatal: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
