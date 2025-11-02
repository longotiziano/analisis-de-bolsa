from app.utils.requests import realizar_request, requests_headers
from bs4 import BeautifulSoup
import requests
from typing import Tuple

class Dolar:
    """
    Esta clase contiene los objetos del dolar, con sus atributos y métodos
    """
    def __init__(self):
        self.valor = 0

    def web_scrap_dolar(self) -> Tuple[bool, float | None]:
        """
        Realizar web scraping para obtener el valor del dólar desde la página www.dolarhoy.com
        Retorna:
        - (True, valor del dólar) si la extracción fue exitosa
        - (False, None) si ocurrió algún error
        """
        url_web = "https://www.dolarhoy.com/"

        request_ok, soup = realizar_request(url_web, 'html')
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
        
    def obtener_valor_dolar():
        """
        Esta función obtiene el valor del dólar blue del día de hoy, intentando primero en
        una API directa, y en caso de error en la conexión se obtiene desde el HTML de una
        página web
        """
        
x = Dolar()
print(x.web_scrap_dolar())

