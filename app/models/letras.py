from app.utils.requests import realizar_request
import pandas as pd
from typing import Tuple

from logs.loggers import iniciar_logger
log = iniciar_logger(__name__)

class Lecaps:
    """
    Clase para definir las letras de capitalización argentinas  
    """
    url_data912 = "https://data912.com/live/arg_notes"

    def __init__(self):
        pass

    def obtener_df_letras(self) -> Tuple[bool, pd.DataFrame | None]:
        """
        Obtiene capitalizaciones de la API https://data912.com y las devuelve en un DataFrame
        """
        request_ok, lista_lecaps = realizar_request(self.url_data912, 'api')
        if not request_ok:
            # El log ya lo maneja la función auxiliar
            return False, None
        
        lecaps_df = pd.DataFrame(lista_lecaps)
        log.info("LeCAPS y sus capitalizaciones obtenidas exitosamente - LeCAPS encontradas: %s", len(lecaps_df))
        return lecaps_df