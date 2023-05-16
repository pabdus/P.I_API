

# Proyecto de Data Science 1 - HENRY. Proyecto Individual 
                              ![](https://user-images.githubusercontent.com/112780608/238518446-91bc87a4-acc2-43d6-a80d-0ee51b785589.png)

## Descripción del proyecto
Este proyecto tiene como objetivo  realizar un proceso de ETL y EDA a un dataset de películas para poder generar un sistema de recomendación de películas.

# Solicitudes del Proyecto

**Transformaciones:**

Algunos campos, como belongs_to_collection, production_companies y otros (ver diccionario de datos) están anidados, esto es o bien tienen un diccionario o una lista como valores en cada fila, ¡deberán desanidarlos para poder y unirlos al dataset de nuevo hacer alguna de las consultas de la API! O bien buscar la manera de acceder a esos datos sin desanidarlos.

Los valores nulos de los campos revenue, budget deben ser rellenados por el número 0.

Los valores nulos del campo release date deben eliminarse.

De haber fechas, deberán tener el formato AAAA-mm-dd, además deberán crear la columna release_year donde extraerán el año de la fecha de estreno.

Crear la columna con el retorno de inversión, llamada return con los campos revenue y budget, dividiendo estas dos últimas revenue / budget, cuando no hay datos disponibles para calcularlo, deberá tomar el valor 0.

Eliminar las columnas que no serán utilizadas, video,imdb_id,adult,original_title,vote_count,poster_path y homepage.


Desarrollo API: Propones disponibilizar los datos de la empresa usando el framework FastAPI.

Deben crear 6 funciones para los endpoints que se consumirán en la API.



# ETL
Para poder realizar el análisis de las películas, se realizó un **[proceso de ETL](https://github.com/pabdus/P.I_API/blob/main/Procesos/ETL.ipynb)** (Extracción, Transformación y Carga) con los siguientes pasos:

**Extracción**: se obtuvo el dataset de películas desde **[movies_dataset.csv](https://drive.google.com/file/d/1Rp7SNuoRnmdoQMa5LWXuK4i7W1ILblYb/view?usp=sharing)**.

**Transformación**: se eliminaron columnas innecesarias, se convirtieron los tipos de datos a los adecuados y se eliminaron filas con datos faltantes.
Carga: se cargó el dataset limpio en un DataFrame de pandas para su posterior análisis.

# EDA
Una vez cargado el dataset, se procedió a realizar un **[análisis exploratorio de datos (EDA)](https://github.com/pabdus/P.I_API/blob/main/Procesos/EDA.ipynb)**. Este proceso incluyó la creación de visualizaciones para poder entender mejor los datos, así como la realización de una nube de palabras para ver las palabras que se repetían con mayor frecuencia en el título de las películas.

# Machine Learning - Sistema de recomendación
Para poder generar un **[sistema de recomendación de películas](https://github.com/pabdus/P.I_API/blob/main/recomender.py)**, se utilizó el algoritmo de similitud coseno. Este algoritmo se basa en la similitud entre dos vectores, en este caso, los vectores corresponden a las películas.

## El proceso para generar el sistema de recomendación fue el siguiente:

Se creó una matriz de similitud utilizando el algoritmo de **[similitud coseno](s.wikipedia.org/wiki/Similitud_coseno#:~:text=La%20similitud%20coseno%20es%20una,del%20ángulo%20comprendido%20entre%20ellos.)**.
Se utilizó esta matriz para generar una lista de películas recomendadas para cada película en el dataset.

## API


Se creó una API utilizando la librería FastAPI para poder consumir los datos y obtener recomendaciones de películas. **[Codigo API](https://github.com/pabdus/P.I_API/blob/main/main.py)**

## Para utilizar la API, se puede acceder desde el siguiente link:

**[API CONSUMIBLE](https://api-movies-project1.onrender.com/)**


![](https://user-images.githubusercontent.com/112780608/238518451-eeb6d6f8-8edc-4a98-a7f3-ca1930095536.png)

