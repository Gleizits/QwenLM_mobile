"""Configuración del sistema de logging."""

import logging

from ..config import LOGS_DIR

_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _build_formatter() -> logging.Formatter:
    """Construye el formatter estándar del proyecto."""
    return logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)


def setup_logger(name: str, log_file: str = "bot.log") -> logging.Logger:
    """
    Configura y retorna un logger con formato personalizado.

    Args:
        name: Nombre del logger
        log_file: Nombre del archivo de log

    Returns:
        Logger configurado
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    LOGS_DIR.mkdir(exist_ok=True)
    logger.setLevel(logging.INFO)

    formatter = _build_formatter()

    file_handler = logging.FileHandler(LOGS_DIR / log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger