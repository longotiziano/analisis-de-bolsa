from app.utils.requests import realizar_request
from typing import Tuple


from logs.config import LOGGING_CONFIG
from logging.config import dictConfig
import logging
dictConfig(LOGGING_CONFIG)
log = logging.getLogger("project_logger")
print(log.handlers)


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
            return False, None

        # Buscamos el bloque principal del dólar blue
        blue_block = soup.find("div", class_="tile is-child")
        if not blue_block:
            return False, None

        valor_div = blue_block.find("div", class_="val")
        if not valor_div:
            return False, None

        valor_dolar = valor_div.get_text(strip=True)
        
        # Hago la conversión a float
        valor_dolar = float(valor_dolar[1:])
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

x=Dolar()
print(x.valor_venta)
        

