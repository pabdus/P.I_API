# Importo las librerias necesarias para la API de consultas

from sklearn.feature_extraction.text import TfidfVectorizer
from fastapi import FastAPI
from recomender import get_similar_movies
import pandas as pd
from fastapi.responses import HTMLResponse

# Instancio la API y le doy un titulo, una descripcion y un numero de version
app = FastAPI(title = "Proyecto Individual", description="Data 10", version= "1.0.1")

# Definimos un template HTML para nuestro index
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My API</title>
    <style>
        body {
            background-color: #f2f2f2;
            font-family: Arial, sans-serif;
            text-align: center;
        }

        .container {
            margin: 0 auto;
            max-width: 800px;
            padding: 50px;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 5px 10px rgba(0,0,0,0.2);
        }

        h1 {
            font-size: 48px;
            margin-bottom: 20px;
        }

        p {
            font-size: 24px;
            margin-bottom: 50px;
        }

        button {
            background-color: #4CAF50;
            color: white;
            padding: 16px 32px;
            border: none;
            border-radius: 5px;
            font-size: 24px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }

        button:hover {
            background-color: #3e8e41;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to My API</h1>
        <p>Here you can find information about movies and more.</p>
        <button onclick="window.location.href='/docs'">Go to API Documentation</button>
    </div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return template


# cargo mi dataset
df = pd.read_csv('data_limpia.csv')


# convertir la columna "release_date" al tipo de datos datetime
df["release_date"] = pd.to_datetime(df["release_date"], format="%Y-%m-%d")

# crear la columna "day_of_week" con el número del día de la semana (de 0 a 6)
df["day_of_week"] = df["release_date"].dt.dayofweek
df['release_month'] = pd.to_datetime(df['release_date']).dt.month

# creo un diccionario para utilizarlo en la funcion de Mes para que puedan ser consultadas las cantidades en español o en ingles
meses = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12,
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12
}

# Creo la funcion que me devuelve la cantidad de peliculas por mes

@app.get("/peliculas_mes/{Mes_month}")

async def peliculas_mes(Mes_month: str):

    try:
        mes_num = meses.get(Mes_month.lower(), None)
        if mes_num is None:
            raise KeyError()
    except KeyError:
        return {"error": f"El mes '{Mes_month}' no es válido. Por favor, ingrese un mes válido en español o inglés."}
    
    df["release_month"] = pd.DatetimeIndex(df["release_date"]).month
    df_mes = df[df["release_month"] == mes_num]
    cantidad = len(df_mes)

    return {"Mes": Mes_month.title(), "Cantidad": cantidad}
    

# Creo la funcion que me devuleve la cantidad de peliculas por mes y dia
month_dict = {
    "enero": 1, "january": 1,
    "febrero": 2, "february": 2,
    "marzo": 3, "march": 3,
    "abril": 4, "april": 4,
    "mayo": 5, "may": 5,
    "junio": 6, "june": 6,
    "julio": 7, "july": 7,
    "agosto": 8, "august": 8,
    "septiembre": 9, "september": 9,
    "octubre": 10, "october": 10,
    "noviembre": 11, "november": 11,
    "diciembre": 12, "december": 12
}

day_dict = {
    "monday": 0,
    "lunes": 0,
    "tuesday": 1,
    "martes": 1,
    "wednesday": 2,
    "miercoles": 2,
    "thursday": 3,
    "jueves": 3,
    "friday": 4,
    "viernes": 4,
    "saturday": 5,
    "sabado": 5,
    "sunday": 6,
    "domingo": 6
}


def get_movie_count(month: str, day: str) -> int:
    month_num = month_dict.get(month.lower(), None)
    if month_num is None:
        return 0
    
    day_name = day_dict.get(day.lower(), None)
    if day_name is None:
        return 0
    
    mask = (df["release_month"] == month_num) & (df["day_of_week"] == day_name)
    filtered_df = df[mask]
    
    return len(filtered_df)

@app.get("/Peliculas/{month}/{day}")
async def count_movies(month: str, day: str):
    count = get_movie_count(month, day)
    return {"count": count}

# Creo la funcion franquicia que me retorna la cantidad de peliculas, las ganancias totales y la ganancia promedio

@app.get("/franquicia/{franquicia}")
async def info_franquicia(franquicia: str):
    try:
        df_franquicia = df[df["belongs_to_collection_name"].str.lower() == franquicia.lower()]
    except:
        respuesta = {"franquicia": franquicia.capitalize(), "cantidad": 0, "ganancia_total": 0, "ganancia_promedio": 0}
        return respuesta
        
    cantidad = len(df_franquicia)
    ganancia_total = df_franquicia["revenue"].sum()
    ganancia_promedio = df_franquicia["revenue"].mean()
    
    respuesta = {"Franquicia": franquicia.capitalize(), "Cantidad": cantidad, "Ganancia total": ganancia_total, "Ganancia Promedio": ganancia_promedio}
    return respuesta
    


# Función que retorna la cantidad de peliculas por pais
@app.get("/peliculas_pais/{pais}")
async def peliculas_pais(pais: str):
    df_pais = df[df["production_countries_name"] == pais.lower()]
    cantidad = len(df_pais)
    return {"Pais": pais.capitalize(), "Cantidad": cantidad}

# Funcion que retorna en nombre de la productora la ganancia total y la cantidad
@app.get("/productoras/{productora}")
async def productoras(productora: str):
    df_productora = df[df["production_companies_name"].str.lower().str.contains(productora.lower())]
    ganancia_total = df_productora["revenue"].sum()
    cantidad = len(df_productora)
    return {"Productora": productora.capitalize(), "Ganancia Total": ganancia_total, "Cantidad": cantidad}


#Funcion que llama al modelo de ML
@app.get("/recomendacion")
async def Recomendacion(movie_title: str):
    
    recommended_movies =get_similar_movies(movie_title)
    
    return {"Recommended Movies": recommended_movies}


