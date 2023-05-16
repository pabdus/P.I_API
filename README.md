

# Proyecto de Data Science 1 - HENRY. Proyecto Individual 
![](https://user-images.githubusercontent.com/112780608/238518446-91bc87a4-acc2-43d6-a80d-0ee51b785589.png)

##Descripción del proyecto
Este proyecto tiene como objetivo  realizar un proceso de ETL y EDA a un dataset de películas para poder generar un sistema de recomendación de películas.

# Solicitudes del Proyecto

Transformaciones:

Algunos campos, como belongs_to_collection, production_companies y otros (ver diccionario de datos) están anidados, esto es o bien tienen un diccionario o una lista como valores en cada fila, ¡deberán desanidarlos para poder y unirlos al dataset de nuevo hacer alguna de las consultas de la API! O bien buscar la manera de acceder a esos datos sin desanidarlos.

Los valores nulos de los campos revenue, budget deben ser rellenados por el número 0.

Los valores nulos del campo release date deben eliminarse.

De haber fechas, deberán tener el formato AAAA-mm-dd, además deberán crear la columna release_year donde extraerán el año de la fecha de estreno.

Crear la columna con el retorno de inversión, llamada return con los campos revenue y budget, dividiendo estas dos últimas revenue / budget, cuando no hay datos disponibles para calcularlo, deberá tomar el valor 0.

Eliminar las columnas que no serán utilizadas, video,imdb_id,adult,original_title,vote_count,poster_path y homepage.


Desarrollo API: Propones disponibilizar los datos de la empresa usando el framework FastAPI. Las consultas que propones son las siguientes:

Deben crear 6 funciones para los endpoints que se consumirán en la API, recuerden que deben tener un decorador por cada una (@app.get(‘/’)).

def peliculas_mes(mes): '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes (nombre del mes, en str, ejemplo 'enero') historicamente''' return {'mes':mes, 'cantidad':respuesta}

def peliculas_dia(dia): '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrenaron ese dia (de la semana, en str, ejemplo 'lunes') historicamente''' return {'dia':dia, 'cantidad':respuesta}

def franquicia(franquicia): '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio''' return {'franquicia':franquicia, 'cantidad':respuesta, 'ganancia_total':respuesta, 'ganancia_promedio':respuesta}

def peliculas_pais(pais): '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo''' return {'pais':pais, 'cantidad':respuesta}

def productoras(productora): '''Ingresas la productora, retornando la ganancia total y la cantidad de peliculas que produjeron''' return {'productora':productora, 'ganancia_total':respuesta, 'cantidad':respuesta}

def retorno(pelicula): '''Ingresas la pelicula, retornando la inversion, la ganancia, el retorno y el año en el que se lanzo''' return {'pelicula':pelicula, 'inversion':respuesta, 'ganacia':respuesta,'retorno':respuesta, 'anio':respuesta}


Deployment: Conoces sobre Render y tienes un tutorial de Render que te hace la vida mas facil 😄 . Tambien podrias usar Railway, o cualquier otro servicio que permita que la API pueda ser consumida desde la web.



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

![](https://user-images.githubusercontent.com/112780608/238518451-eeb6d6f8-8edc-4a98-a7f3-ca1930095536.png)

