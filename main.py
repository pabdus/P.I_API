# Importo las librerias necesarias para la API de consultas
from sklearn.feature_extraction.text import TfidfVectorizer
from fastapi import FastAPI
from recomender import get_similar_movies
import pandas as pd
from fastapi.responses import HTMLResponse


# Instancio la API y le doy un titulo, una descripcion y un numero de version
app = FastAPI(title="Proyecto Individual", description="Data 10", version="1.0.1")

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
@app.get("/peliculas_mes/{mes}")
async def peliculas_mes(mes: str):
    try:
        mes_num = meses[mes.lower()]
    except KeyError:
        return {"error": f"El mes '{mes}' no es válido. Por favor, ingrese un mes válido en español o inglés."}
    df_mes = df[df["release_date"].str.contains(f"-{mes_num}-")]
    cantidad = len(df_mes)
    return {"Mes": mes.title(), "Cantidad": cantidad}
    

# Creo la funcion que me devuleve la cantidad de peliculas por dia

dias_semana = {
    'lunes': 'Monday',
    'martes': 'Tuesday',
    'miercoles': 'Wednesday',
    'jueves': 'Thursday',
    'viernes': 'Friday',
    'sabado': 'Saturday',
    'domingo': 'Sunday'
}

@app.get("/peliculas_dia/{dia}")
async def peliculas_dia(dia: str):
    dia = dia.lower()
    if dia not in dias_semana:
        return {"error": f"El día '{dia}' no es válido. Por favor, ingrese un día válido en español."}
    
    dia_ingles = dias_semana[dia]
    df_dia = df[df['release_day'] == dia_ingles]
    cantidad = len(df_dia)
    
    return {"Cantidad": cantidad, "Dia": dia.capitalize()}

# funcion score

@app.get("/score_titulo/{titulo_de_la_filmacion}")
async def score_titulo(titulo_de_la_filmacion: str):
    pelicula = df[df['title'].str.lower() == titulo_de_la_filmacion.lower()]
    if pelicula.empty:
        return {'mensaje': 'No se encontró la película'}
    else:
        titulo = pelicula['title'].values[0]
        año_estreno = pelicula['release_year'].values[0]
        score = pelicula['popularity'].values[0]
        return {'titulo': str(titulo), 'año_estreno': str(año_estreno), 'score': str(score)}

# funcion votos
@app.get("/votos_titulo/{titulo_de_la_filmacion}")
async def votos_titulo(titulo_de_la_filmacion: str):
    pelicula = df[df['title'].str.lower() == titulo_de_la_filmacion.lower()]
    if pelicula.empty:
        return {'mensaje': 'No se encontró la película'}
    else:
        votos = pelicula['vote_count'].values[0]
        promedio = pelicula['vote_average'].values[0]
        if votos >= 2000:
            titulo = pelicula['title'].values[0]
            año_estreno = pelicula['release_year'].values[0]
            return {'titulo': str(titulo), 'año_estreno': str(año_estreno), 'votos': str(votos), 'promedio': str(promedio)}
        else:
            return {'mensaje': 'La película no cumple con el requisito de tener al menos 2000 valoraciones'}

@app.get("/get_actor/{nombre_actor}")
async def get_actor(nombre_actor: str):
    df['actores'] = df['actores'].apply(lambda actores: eval(actores) if isinstance(actores, str) else actores)
    actor_films = df[df['actores'].apply(lambda actores: isinstance(actores, list) and any(nombre_actor.lower() in a.lower() for a in actores))]

    if actor_films.empty:
        return {'mensaje': 'No se encontró al actor en ninguna filmación'}
    else:
        cantidad_films = len(actor_films)
        retorno_total = actor_films['revenue'].sum()
        promedio_retorno = round(actor_films['revenue'].mean(),2)
        return {
            'actor': nombre_actor,
            'cantidad_films': cantidad_films,
            'retorno_total': retorno_total,
            'promedio_retorno': promedio_retorno
        }
    
@app.get("/get_director/{nombre_director}")
async def get_director(nombre_director: str):
    director_films = df[df['director'].str.lower() == nombre_director.lower()]

    if director_films.empty:
        return {'mensaje': 'No se encontró al director en ninguna filmación'}
    else:
        nombre_peliculas = director_films['title'].tolist()
        fechas_lanzamiento = director_films['release_date'].tolist()
        retornos_individuales = director_films['return'].tolist()
        costos = director_films['budget'].tolist()
        ganancias = director_films['revenue'].tolist()

        return {
            'director': nombre_director,
            'peliculas': [
                {
                    'nombre_pelicula': nombre,
                    'fecha_lanzamiento': fecha,
                    'retorno_individual': retorno,
                    'costo': costo,
                    'ganancia': ganancia
                }
                for nombre, fecha, retorno, costo, ganancia in zip(nombre_peliculas, fechas_lanzamiento, retornos_individuales, costos, ganancias)
            ]
        }

#Funcion que llama al modelo de ML
@app.get("/recomendacion")
async def Recomendacion(movie_title: str):
    
    recommended_movies =get_similar_movies(movie_title)
    
    return {"Recommended Movies": recommended_movies}


