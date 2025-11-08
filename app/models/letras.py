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


    def _calcular_tna(
            self, 
            tirea: float | None,
            valor_vto: float | None, 
            precio_actual: float | None, 
            plazo_dias: int | None
            ) -> float | None:
        """
        Devuelve la TNA (Tasa Nominal Anual) de una letra.
        - Si se proporciona la TIREA (tasa efectiva anual), la convierte directamente.
        - Si no, la calcula a partir del valor de vencimiento, precio actual y plazo en días.
        """
        if tirea:
            # Primero calculo la TEM y, con ese dato, la TNA
            tem = (1 + tirea) ** (1/12) - 1 
            tna = tem * 12 
            log.debug('TNA calculada -> TEM: %s | TNA: %s', tem, tna)
            return tna

        # Me aseguro que no haya faltantes
        valores = {
        "valor_vto": valor_vto,
        "precio_actual": precio_actual,
        "plazo_dias": plazo_dias
        }

        faltantes = [n for n, v in valores.items() if v is None]
        if faltantes:
            log.warning('No se pudo calcular la TNA de la LECAP, faltan los datos: %s', ", ".join(faltantes))
            return None
        
        # Este bloque de código quedó sin testear debido a no encontrar la información
        tna = ((valor_vto / precio_actual) - 1) * (365 / plazo_dias)
        log.debug(
        "TNA calculada -> valor_vto: %.2f | precio_actual: %.2f | plazo_dias: %d | TNA: %.4f",
        valor_vto, precio_actual, plazo_dias, tna
        )
        return tna
    

    def _obtener_tirea(self) -> Tuple[bool, pd.DataFrame | None]:
        """
        Obtengo la TIREA (tasa efectiva anual) de LECAPs mediante scraping a la página oficial del gobierno
        de la Argentina, buscando aquellas noticias con título "Resultado de licitación", donde dentro de
        esos sitios se encontrarán las diversas TIREAs
        """
        request_ok, soup = realizar_request(self.url_gob_argentina, 'html')
        if not request_ok:
            # El log ya lo maneja la función auxiliar
            return False, None
        
        # Palabras clave que quiero encontrar en las noticias
        palabras_clave = ['resultado', 'licitacion', 'lecap']

        id_noticias = 'divnoticias'
        block_noticias = soup.find("div", id=id_noticias)
        if not block_noticias:
            log.error('No se encontró el bloque: %s - URL: %s', id_noticias, self.url_gob_argentina)
            return False, None
        
        filas_noticias = block_noticias.find_all("div", class_="row panels-row")
        print(len(filas_noticias))


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

        # Calculo TNA
        df_letras_limpio["tna"] = df_letras_limpio.apply(
            lambda row: self._calcular_tna(100.0, row["precio"], row["plazo_dias"]), axis=1
        )

        return df_letras_limpio[["letra", "precio", "vencimiento", "plazo_dias", "tna"]].sort_values(by="plazo_dias", ascending=True)