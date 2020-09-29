import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pickle
from os import path

import time
start_time = time.time()


# Importar datos limpios
df = pd.read_csv('src/metadata_ready.csv', low_memory=False, encoding = 'unicode_escape')
df.head()
# Importar todos los datos
orig_df = pd.read_csv('src/movies_metadata.csv', low_memory=False, encoding = 'unicode_escape')

# Se agregan las características dentro de los datos limpios
print('Agregando las características dentro de los datos limpios')
df['overview'], df['id'] = orig_df['overview'], orig_df['id']
df.head()

# Remover las STOPWORDS
tfidf = TfidfVectorizer(stop_words='english')
# Reemplazar los NaN por datos vacíos
df['overview'] = df['overview'].fillna('')

# Construción de la matriz TF-IDF aplicando el método fit_transform en la función de descripción general
tfidf_matrix = tfidf.fit_transform(df['overview'])
tfidf_matrix.shape

cosine_sim = None
indices = None

# Preparar la matriz similitud coseno
print('INICIA SIMILITUD COSENO')
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
# cosine_sim = pickle.load(open("src/cosine_sim.txt", "rb"))
# if(path.exists("src/cosine_sim.txt")):
#     print("Existe fichero")
# else:
#     print('No existe fichero')
#     cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
#     print('Se crea el archivo con el algoritmo entrenado')
#     pickle.dump(cosine_sim, open("src/cosine_sim.txt", "wb"), protocol=4)

# Construción de un mapeo inverso de índices y títulos de películas, y limpiar títulos duplicados, si es que existen
print("CREACIÓN DE ÍNDICES")
if(path.exists('/src/indices,txt')):
    print('Existe fichero')
    indices = pickle.load(open("src/indices.txt", "rb"))
else:
    print('No existe fichero')
    indices = pd.Series(df.index, index=df['genres']).drop_duplicates()
    print('Se crea el archivo con los índices')
    pickle.dump(indices, open("src/indices.txt", "wb"), protocol=4)




# Función que toma el título de la película como entrada y da recomendaciones
def content_recommender(genres, cosine_sim=cosine_sim, df=df, indices=indices):
    print('INICIA RECOMENDADOR')
    # Obtain the index of the movie that matches the title
    idx = indices[genres]

    # Get the pairwsie similarity scores of all movies with that movie
    # And convert it into a list of tuples as described above
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies based on the cosine similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies. Ignore the first movie.
    sim_scores = sim_scores[1:11]

    # Get the movie indices
    movie_indices = [i[0] for i in sim_scores]

    # Return the top 10 most similar movies
    return df['title'].iloc[movie_indices]

print(content_recommender("['action']"))
print(time.time() - start_time)