# Manejo de errores y loggeo
- Con respecto al manejo de errores, decidí manejar aquellos que no necesariamente tienen que romper el flujo del programa 
con retornos de tuplas de tipo booleano y valor.
* La estrategia de logging es la siguiente:
    - **DEBUG**: Colocados en funciones auxiliares
    - **INFO**
    - **WARNING**
    - **ERROR**: Se desarrollarán en las funciones auxiliares y pequeñas, de manera tal que capturen el error lo antes posible
    - **CRITICAL**
- Al momento de orquestar el flujo con Airflow, simplemente agregamos a su sistema de logging el header `file_csv`.