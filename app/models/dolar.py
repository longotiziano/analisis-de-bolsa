from bs4 import BeautifulSoup
import requests

class Dolar:
    """
    Esta clase contiene los objetos del dolar, con sus atributos y métodos
    """
    def __init__(self):
        pass

    def obtener_cotizacion_api(self):
        '''
        Obtengo la cotización del dólar en pesos argentinos desde la API de Dolarsi
        '''
        url_api = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"

        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            response = requests.get(url_api, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()
            print(data)
        except requests.exceptions.RequestException as e:
            print("Error en la request:", e)

x = Dolar()
x.obtener_cotizacion_api()
