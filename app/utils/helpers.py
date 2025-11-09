from datetime import date

from logs.loggers import iniciar_logger
log = iniciar_logger(__name__)

def obtener_plazo_dias(fecha: date) -> int:
    """
    Helper que calcula los días faltantes desde hoy hasta una fecha introducida
    """
    return (fecha - date.today()).days

def calcular_tna( 
        tirea: float | None,
        valor_vto: float | None, 
        precio_actual: float | None, 
        plazo_dias: int | None
        ) -> float | None:
    """
    Devuelve la TNA (Tasa Nominal Anual) de una letra.
    - Si se proporciona la TIREA (tasa efectiva anual), la convierte directamente.
    - Si no, la calcula a partir del valor de vencimiento, precio actual y plazo en días.

    -> Esta función no fue utilizada en la finalización del proyecto
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