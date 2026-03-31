"""Configuración del sistema de logging."""

import logging
from pathlib import Path


def setup_logger(name: str, log_file: str = "bot.log") -> logging.Logger:
    """
    Configura y retorna un logger con formato personalizado.
    
    Args:
        name: Nombre del logger
        log_file: Nombre del archivo de log
        
    Returns:
        Logger configurado
    """
    logs_dir = Path(__file__).parent.parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evitar duplicar handlers
    if logger.handlers:
        return logger
    
    # Formato del log
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Handler para archivo
    file_handler = logging.FileHandler(logs_dir / log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger
