from bs4 import BeautifulSoup
import requests 
from typing import Any, Literal, Tuple

from logs.loggers import iniciar_logger
log = iniciar_logger(__name__)

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
    try:
        response = requests.get(url, headers=requests_headers, timeout=(5, 10))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        log.exception("Error durante la request a %s", url)
        return False, None

    # En caso de tratarse de una request a una API
    if tipo_request == 'api':    
        try:
            data = response.json()
        except ValueError:
            log.error("Error durante la codificación a JSON. Respuesta: %s", response.text[:200])
            return False, None
    
    # Y en caso de buscar web scraping
    elif tipo_request == 'html':
        data = BeautifulSoup(response.text, 'lxml')
    else:
        log.error("Tipo de request inválido: %s", tipo_request)
        return False, None
    
    log.info("Request realizada correctamente - tipo: %s - URL: %s", tipo_request, url)
    return True, data
