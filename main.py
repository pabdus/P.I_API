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

# creo un diccionario para utilizarlo en la funcion de Mes para que puedan ser consultadas las cantidades en español o en ingles
meses = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12",
    "january": "01",
    "february": "02",
    "march": "03",
    "april": "04",
    "may": "05",
    "june": "06",
    "july": "07",
    "august": "08",
    "september": "09",
    "october": "10",
    "november": "11",
    "december": "12"
}

# Creo la funcion que me devuelve la cantidad de peliculas por mes
@app.get("/peliculas_mes/{Mes/Month}")
async def peliculas_mes(Mes_month: str):
    try:
        mes_num = meses[Mes_month.lower()]
    except KeyError:
        return {"error": f"El mes '{Mes_month}' no es válido. Por favor, ingrese un mes válido en español o inglés."}
    df_mes = df[df["release_date"].str.contains(f"-{mes_num}-")]
    cantidad = len(df_mes)
    return {"Mes": Mes_month.title(), "Cantidad": cantidad}
    

# Creo la funcion que me devuleve la cantidad de peliculas por dia

@app.get("/peliculas_dia/{dia}")
async def peliculas_dia(dia: str):
    try:
        dia_num = int(dia)
    except ValueError:
        return {"error": f"El día '{dia}' no es válido. Por favor, ingrese un número de día válido (1-31)."}
    if dia_num < 1 or dia_num > 31:
        return {"error": f"El día '{dia}' no es válido. Por favor, ingrese un número de día válido (1-31)."}
    df_dia = df[df["release_date"].str.endswith(f"-{dia_num:02d}")]
    cantidad = len(df_dia)
    return {"Dia": dia, "Cantidad": cantidad}

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

