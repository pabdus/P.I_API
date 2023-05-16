![](https://user-images.githubusercontent.com/112780608/238518446-91bc87a4-acc2-43d6-a80d-0ee51b785589.png)

# Proyecto de Data Science - Análisis de películas
Descripción del proyecto
Este proyecto tiene como objetivo analizar un dataset de películas para poder generar un sistema de recomendación de películas utilizando el algoritmo de similitud coseno.

# ETL
Para poder realizar el análisis de las películas, se realizó un proceso de ETL (Extracción, Transformación y Carga) con los siguientes pasos:

Extracción: se obtuvo el dataset de películas desde [fuente de datos].
Transformación: se eliminaron columnas innecesarias, se convirtieron los tipos de datos a los adecuados y se eliminaron filas con datos faltantes.
Carga: se cargó el dataset limpio en un DataFrame de pandas para su posterior análisis.
# EDA
Una vez cargado el dataset, se procedió a realizar un análisis exploratorio de datos (EDA). Este proceso incluyó la creación de visualizaciones para poder entender mejor los datos, así como la realización de una nube de palabras para ver las palabras que se repetían con mayor frecuencia en el título de las películas.

# Machine Learning - Sistema de recomendación
Para poder generar un sistema de recomendación de películas, se utilizó el algoritmo de similitud coseno. Este algoritmo se basa en la similitud entre dos vectores, en este caso, los vectores corresponden a las películas.

## El proceso para generar el sistema de recomendación fue el siguiente:

Se creó una matriz de similitud utilizando el algoritmo de similitud coseno.
Se utilizó esta matriz para generar una lista de películas recomendadas para cada película en el dataset.
Se creó una API utilizando la librería FastAPI para poder consumir los datos y obtener recomendaciones de películas.
Uso de la API
## Para utilizar la API, se pueden seguir los siguientes pasos:

Clonar el repositorio desde GitHub.
Instalar las dependencias necesarias.
Correr la aplicación.
Consumir los endpoints para obtener recomendaciones de películas.
En resumen, este proyecto tiene como objetivo analizar un dataset de películas y generar un sistema de recomendación de películas utilizando el algoritmo de similitud coseno. Todo esto se ha implementado en una API utilizando la librería FastAPI para poder acceder a las recomendaciones desde cualquier lugar.

![] (https://user-images.githubusercontent.com/112780608/238518451-eeb6d6f8-8edc-4a98-a7f3-ca1930095536.png)

