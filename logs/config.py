import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_LOG_FILE = BASE_DIR / "logs" / "logs.csv"

if not os.path.exists(CSV_LOG_FILE):
    with open(CSV_LOG_FILE, "w", newline="") as f:
        f.write('"timestamp","logger","level","message"\n')

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,  # No desactiva loggers ya existentes
    "formatters": {
        "csv": {
            "format": '"%(asctime)s","%(name)s","%(levelname)s","%(message)s"'
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
    },
    "handlers": {
        "console": {  # Handler que imprime en consola
            "class": "logging.StreamHandler",
            "formatter": "detailed",  # Usa el formatter definido arriba
            "level": "DEBUG",  # Nivel mínimo que se imprime en consola
        },
        "csv_file": {  # Handler que escribe en archivo
            "class": "logging.FileHandler",
            "formatter": "csv",
            "filename": CSV_LOG_FILE,
            "level": "DEBUG",
            "mode": "a",
        },
    },
    "loggers": {
        "project_logger": {
            "handlers": ["console", "csv_file"],
            "level": "DEBUG",  # Nivel mínimo del logger
            "propagate": True  # Propaga logs a loggers padres
        }
    }
}