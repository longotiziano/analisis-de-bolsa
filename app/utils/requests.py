from bs4 import BeautifulSoup
import requests 
from typing import Any, Literal, Tuple

requests_headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}

def realizar_request(
    url: str, 
    tipo_request: Literal['html', 'api']
) -> Tuple[bool, Any | None]:
    """
    Función auxiliar para realizar requests HTTP y manejar errores de forma centralizada.
    Retorna:
    - (True, data) si la request fue exitosa
    - (False, None) si ocurrió algún error
    """
    #"https://www.dolarsi.com/api/api.php?type=valoresprincipales"
        
    try:
        response = requests.get(url, headers=requests_headers, timeout=(5, 10)) # espera de conexión y respuesta respectivamente
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return False, None

    if tipo_request == 'api':    
        try:
            data = response.json()
        except ValueError:
            print("[ERROR] No se pudo decodificar JSON.")
            return False, None
    
    if tipo_request == 'html':
        data = BeautifulSoup(response.text, 'html.parser')
    
    return True, data
