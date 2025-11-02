from logging.config import dictConfig
import logging
from .config import LOGGING_CONFIG

def get_logger(name: str = "project_logger") -> logging.Logger:
    """
    Obtengo el logger para registrar eventos
    """
    dictConfig(LOGGING_CONFIG)
    return logging.getLogger(name)