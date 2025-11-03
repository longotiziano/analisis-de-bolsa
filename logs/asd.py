import logging
import logging.config
from logs.config import LOGGING_CONFIG  # 👈 cambia 'logger_setup' por el nombre real del archivo donde está tu config

# Aplicar la configuración
logging.config.dictConfig(LOGGING_CONFIG)

# Obtener el logger
logger = logging.getLogger("project_logger")

# Probar logs
logger.debug("Mensaje DEBUG")
logger.info("Mensaje INFO")
logger.warning("Mensaje WARNING")
logger.error("Mensaje ERROR")
