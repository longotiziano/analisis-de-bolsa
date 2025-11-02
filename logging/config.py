LOGGING_CONFIG = {
    "version": 1,  # Siempre 1
    "disable_existing_loggers": False,  # No desactiva loggers ya existentes
    "formatters": {
        "detailed": {  # Nombre del formateador
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {  # Handler que imprime en consola
            "class": "logging.StreamHandler",
            "formatter": "detailed",  # Usa el formatter definido arriba
            "level": "INFO",  # Nivel mínimo que se imprime en consola
        },
        "file": {  # Handler que escribe en archivo
            "class": "logging.FileHandler",
            "formatter": "detailed",
            "filename": "logs.log",
            "level": "DEBUG",  # Guarda incluso mensajes de debug
        },
    },
    "loggers": {
        "project_logger": {  # El logger que vas a usar en tu proyecto
            "handlers": ["console", "file"],  # Usa estos handlers
            "level": "DEBUG",  # Nivel mínimo del logger
            "propagate": False  # No propaga logs a loggers padres
        }
    }
}