import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Cargar el dataset
df = pd.read_csv('Data_ML.csv')

# Seleccionar las columnas relevantes
df = df[['original_title', 'overview', 'genres_name', 'popularity']]
df = df.dropna()
df = df.sort_values('popularity', ascending=False).iloc[:5500]
df.reset_index(inplace=True, drop=True)

# Limpiar el texto y los géneros
df['overview'] = df['overview'].fillna('')
df['overview'] = df['overview'].apply(lambda x: x.lower())
df['genres_name'] = df['genres_name'].fillna('')
df['genres_name'] = df['genres_name'].apply(lambda x: x.lower())

# Combinar las columnas de texto y géneros en una sola columna
df['combined_features'] = df['overview'] + ' ' + df['genres_name']

# Vectorizar el texto combinado
vectorizer = TfidfVectorizer(stop_words='english')
feature_matrix = vectorizer.fit_transform(df['combined_features'])

# Calcular la similitud de coseno entre las películas
similarity_matrix = cosine_similarity(feature_matrix)

# Obtener las películas más similares a una dada
def get_similar_movies(movie_title, n=5):
    # Buscar la película en el dataset
    try:
        movie_index = df[df['original_title'].str.lower() == movie_title.lower()].index[0]
    except IndexError:
        return f"Lo siento, no se encuentra la película '{movie_title}' en el sistema de recomendaciones."
    
    # Calcular la similitud de la película con el resto de películas
    similar_movies = list(enumerate(similarity_matrix[movie_index]))
    similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)
    
    # Obtener los títulos de las películas más similares
    similar_movies = similar_movies[1:n+1]
    similar_movies = [df.iloc[movie[0]]['original_title'] for movie in similar_movies]
    return similar_movies
