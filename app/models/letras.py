from app.utils.helpers import obtener_plazo_dias
from app.utils.requests import realizar_request
from datetime import date
import pandas as pd
from typing import Tuple

from logs.loggers import iniciar_logger
log = iniciar_logger(__name__)

class Lecaps:
    """
    Clase para definir las letras de capitalización argentinas  
    """
    url_data912 = "https://data912.com/live/arg_notes"
    url_gob_argentina = "https://www.argentina.gob.ar/economia/noticias"
    url_acuantoesta = "https://www.acuantoesta.com.ar/lecaps"

    def __init__(self):
        pass


    def _obtener_df_letras(self) -> Tuple[bool, pd.DataFrame | None]:
        """
        Obtiene capitalizaciones de la API https://data912.com y las devuelve en un DataFrame
        """
        request_ok, lista_lecaps = realizar_request(self.url_data912, 'api')
        if not request_ok:
            # El log ya lo maneja la función auxiliar
            return False, None
        
        lecaps_df = pd.DataFrame(lista_lecaps)
        log.info("LeCAPS y sus capitalizaciones obtenidas exitosamente - LECAPs encontradas: %s", len(lecaps_df))
        return True, lecaps_df
    

    def _desarmar_letra(self, letra: str) -> Tuple[bool, date | None]:
        """
        Desarma la string de la letra y obtiene su fecha de vencimiento
        """
        # Ejemplo: S28N5 → día=28, mes='N', año='5'
        try:
            dia = int(letra[1:3])
            letra_mes = letra[3].upper()
            año = 2020 + int(letra[4])
        except ValueError:
            log.warning('No se ha podido identificar correctamente a la letra: %s', letra)
            return False, None

        # Utilizo un diccionario para obtener el mes de la letra (bolsa argentina)
        letra_a_mes = {
            "E": 1,   # Enero 
            "F": 2,   # Febrero
            "M": 3,   # Marzo
            "A": 4,   # Abril
            "Y": 5,   # Mayo
            "J": 6,   # Junio
            "L": 7,   # Julio
            "G": 8,   # Agosto
            "S": 9,   # Septiembre
            "O": 10,  # Octubre
            "N": 11,  # Noviembre
            "D": 12   # Diciembre
        }

        mes = letra_a_mes.get(letra_mes)
        if mes is None:
            log.warning('No se ha encontrado el mes correspondiente a la letra: %s - Utilizando: "%s"', letra, letra_mes)
            return False, None
        
        log.debug("Letra %s -> %s/%s/%s", letra, dia, mes, año)
        return True, date(año, mes, dia)
    

    def _scrapear_df_letras(self) -> Tuple[bool, pd.DataFrame | None]:
        """
        Realiza un scraping de la página dinámica https://www.acuantoesta.com.ar/lecaps para
        obtener un DataFrame con más información.
        """
        

    def procesar_df_letras(self, df_letras: pd.DataFrame) -> pd.DataFrame:
        """
        Dejo el DataFrame con los valores que me interesan y calculo su TNA con la ayuda
        de las funciones auxiliares realizadas
        """
        df_letras_limpio = pd.DataFrame()
        df_letras_limpio["letra"] = df_letras["symbol"]
        df_letras_limpio["precio"] = df_letras["c"]

        # Aplico desarme de letras y manejo de retorno
        resultados = df_letras["symbol"].apply(self._desarmar_letra)
        df_letras_limpio["ok"] = resultados.apply(lambda x: x[0])
        df_letras_limpio["vencimiento"] = resultados.apply(lambda x: x[1])

        # Filtro solo las letras válidas
        df_letras_limpio = df_letras_limpio[df_letras_limpio["ok"]]

        # Calculo plazo en días
        df_letras_limpio["plazo_dias"] = df_letras_limpio["vencimiento"].apply(obtener_plazo_dias)

        return df_letras_limpio[["letra", "precio", "vencimiento", "plazo_dias", "tna"]].sort_values(by="plazo_dias", ascending=True)