import typer
from loguru import logger
from src.config import settings

from src.core.orchestrator import BridgeOrchestrator

app = typer.Typer(help="Qwen Mobile Bridge - Control Qwen via WhatsApp")

@app.command()
def start():
    """Inicia el servicio de puente entre WhatsApp y Qwen."""
    logger.info("Iniciando Qwen Mobile Bridge")
    orchestrator = BridgeOrchestrator()
    orchestrator.run()

if __name__ == "__main__":
    app()
