# Análisis de bolsa
Este es mi primer proyecto luego de finalizar el curso de ingeniería de datos, donde pondré en práctica mis habilidades y 
todo lo aprendido a lo largo de estos meses. Se me fue ocurrido debido a una necesidad de la optimización de inversiones
personales, organización y curiosidad sobre el area.

## El programa en sí mismo
* Los **objetivos del programa** son obtener las capitalizaciones de distintos activos o para diversas alertas, tales como:
    - LECAPs, bonos argentinos, plazos fijos y TNAs de billeteras virtuales
    - Bajadas drásticas u oportunidades de compra en diversos índices o acciones
    - Análisis de posible cambio de divisa de dólares a pesos y posibilidades de carry trade
    - Alertar sobre noticias importantes que puedan afectar el rumbo
* Y, por supuesto, implementando varias de las tecnologías aprendidas en el curso:
    - Manejo del flujo con **Airflow** que permita un orden y análisis del pipeline
    - Web Scraping con **Python**, como también la lógica central
    - **PostgreSQL** como base de datos, debido a una alta integración con diversas tecnologías y el tratarse de un sistema
    principalmente de lectura
    - Containerización con **Docker**, para un flujo lo más profesional posible
    - Generación de gráficos automática con **Seaborn y matplotlib**
    - Uso de **PySpark** para el procesamiento de datos 