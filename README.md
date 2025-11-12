# Análisis de bolsa
Este es mi primer proyecto luego de finalizar el curso de ingeniería de datos, donde pondré en práctica mis habilidades y 
todo lo aprendido a lo largo de estos meses. Se me fue ocurrido debido a una necesidad de la optimización de inversiones
personales, organización y curiosidad sobre el area.

Este proyecto busca automatizar el seguimiento de activos financieros argentinos y asistir en la toma de decisiones de inversión mediante análisis cuantitativo y visualización de datos en tiempo real.

## El programa en sí mismo
* Los **objetivos del programa** son:
    1. Obtener capitalizaciones de LECAPs, bonos argentinos, plazos fijos y TNAs de billeteras virtuales
    2. Detectar bajadas drásticas u oportunidades de compra en diversos índices o acciones
    3. Análisis de posible cambio de divisa de dólares a pesos y posibilidades de carry trade
    4. Alertar sobre noticias importantes que puedan afectar el rumbo
    5. Conexión con mi billetera y recomendaciones de inversión, con incluso modelos ML
    6. Generación de gráficos explicativos de evolución monetaria

* Y, por supuesto, implementando varias de las tecnologías aprendidas en el curso:
    - Manejo del flujo con **Airflow** que permita un orden y análisis del pipeline
    - Web Scraping con **Python**, como también la lógica central
    - **PostgreSQL** como base de datos, debido a una alta integración con diversas tecnologías y el tratarse de un sistema
    principalmente de lectura
    - Containerización con **Docker**, para un flujo lo más profesional posible
    - Generación de gráficos automática con **Apache Superset**
    - Uso de **PySpark** para el procesamiento de datos 

