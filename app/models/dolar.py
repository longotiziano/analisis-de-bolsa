from app.utils.requests import realizar_request
from typing import Tuple

from logs.loggers import iniciar_logger
log = iniciar_logger(__name__)

class Dolar:
    """
    Esta clase contiene los objetos del dolar, con sus atributos y métodos
    """
    url_dolarhoy = "https://www.dolarhoy.com/"
    url_dolarapi = "https://dolarapi.com/v1/dolares/blue"

    def __init__(self):
        _, self.valor_venta = self.obtener_dolar_api() 

    def web_scrap_dolar(self) -> Tuple[bool, float | None]:
        """
        Realizar web scraping para obtener el valor del dólar desde la página www.dolarhoy.com
        Retorna:
        - (True, valor del dólar) si la extracción fue exitosa
        - (False, None) si ocurrió algún error
        """
        request_ok, soup = realizar_request(self.url_dolarhoy, 'html')
        if not request_ok:
            # El log ya lo maneja la función auxiliar
            return False, None

        # Buscamos el bloque principal del dólar blue
        block_find = "tile is-child"
        blue_block = soup.find("div", class_=block_find)
        if not blue_block:
            log.error('No se encontró el bloque: %s - URL: %s', block_find, self.url_dolarhoy)
            return False, None

        block_find = "val"
        valor_div = blue_block.find("div", class_=block_find)
        if not valor_div:
            log.error('No se encontró el bloque: %s - URL: %s', block_find, self.url_dolarhoy)
            return False, None
        
        # Intento la conversión a float
        try:
            valor_dolar = valor_div.get_text(strip=True)
            valor_dolar = float(valor_dolar[1:])
        except Exception as e:
            log.exception("Error al convertir el valor del dólar - URL: %s - error: %s", self.url_dolarhoy, e)
            return False, None
        
        log.info("Scraping realizado correctamente - bloque: %s - URL: %s", block_find, self.url_dolarhoy)
        return True, valor_dolar
        
    def obtener_dolar_api(self) -> Tuple[bool, float | None]: 
        """
        Esta función obtiene el valor del dólar blue del día de hoy, realizando
        una conexión con la API de www.dolar.api
        """
        request_ok, data = realizar_request(self.url_dolarapi, 'api')
        if not request_ok:
            return False, None
        
        dolar_venta = float(data.get("venta"))
        return True, dolar_venta
        

