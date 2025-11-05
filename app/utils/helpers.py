from datetime import date

def obtener_plazo_dias(fecha: date) -> int:
    """
    Helper que calcula los días faltantes desde hoy hasta una fecha introducida
    """
    return (fecha - date.today()).days