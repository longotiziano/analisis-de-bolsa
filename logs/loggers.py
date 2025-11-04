import logging

def iniciar_logger(name: str = "project_logger") -> logging.Logger:
    """
    Obtengo el logger para registrar eventos
    """    
    logger = logging.getLogger(name)
    logger.propagate = True
    return logger