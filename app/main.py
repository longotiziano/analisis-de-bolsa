# Este bloque va en el archivo principal desde el cual se ejecuta el código
from logs.config import LOGGING_CONFIG
from logging.config import dictConfig
dictConfig(LOGGING_CONFIG)

from app.models.letras import Lecaps
lecap = Lecaps()
ok, df = lecap._obtener_df_letras()
print(lecap.procesar_df_letras(df))