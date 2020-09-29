# Dependencias
import pandas as pd
import numpy as np
from os import path
import pickle, json
from ast import literal_eval


# Clase recommender
class recomendador_categoria:
    # Ruta al dataset
    df = pd.read_csv('src/movies_metadata.csv', low_memory=False, encoding='unicode_escape')
    gen_df = None

    # Constructor
    def __init__(self):
        if(path.exists('src/metadata_clear.csv')):
            self.gen_df = pd.read_csv('src/metadata_clear.csv', low_memory=False, encoding='unicode_escape')
        else:
            cols = self.df.columns
            self.df = self.df[['title', 'genres', 'release_date','runtime', 'vote_average', 'vote_count']]
            head = self.df.head()

            # Conversión de fechas a formato admitido por Pandas
            self.df['release_date'] = pd.to_datetime(self.df['release_date'], errors='coerce')

            # Agregar columna year al dataframe
            self.df['year'] = self.df['release_date'].apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
            # Solución a los valores NaT en las fechas de la columna release_date
            self.df['year'] = self.df['year'].apply(self.fechas_int)

            # Eliminar columna release_date
            self.df = self.df.drop('release_date', axis=1)

            self.df['genres'] = self.df['genres'].fillna('[]')
            self.df['genres'] = self.df['genres'].apply(literal_eval)
            self.df['genres'] = self.df['genres'].apply(lambda x: [i['name'].lower() for i in x] if isinstance(x, list) else [])
            dataframe = self.df.head()

            # Ajuste de la categoría géneros del dataframe
            s = self.df.apply(lambda x: pd.Series(x['genres']), axis=1).stack().reset_index(level=1, drop=True)
            s.name = 'genre'
            self.gen_df = self.df.drop('genres', axis=1).join(s)
            self.gen_df.to_csv('src/metadata_clear.csv',index=False)




    def obtener_recomendaciones(self, feature, params, percentile=0.8):
        feature = feature
        movies_list = pd.Series([],dtype=pd.StringDtype())
        # gen_list = literal_eval(params)
        gen_list = params
        
        # Recorrer los géneros para la construcción la lista
        for i in gen_list:
            movies = self.gen_df.copy()
            movies = movies[(movies[feature] == i) ]

            C = movies['vote_average'].mean()
            m = movies['vote_count'].quantile(percentile)
            q_movies = movies.copy().loc[movies['vote_count'] >= m]
            
            # Calcular el score usando la forumal de IMDB
            q_movies['score'] = q_movies.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average'])+ (m/(m+x['vote_count']) * C), axis=1)
            q_movies = q_movies.sort_values('score', ascending=False)
            q_movies = q_movies[1:21]

            movies_list = pd.concat([movies_list,q_movies])
        
        movies_list.drop(movies_list.columns[0], axis=1, inplace=True)
        movies_list.drop(movies_list.columns[0], axis=1, inplace=True)
        movies_list.sort_values('score',ascending=False)
        movies_list = movies_list.drop_duplicates(subset=['title'])
        
        return movies_list.to_dict('records')

    # Función de apoyo al tratamiento de fechas en el dataframe
    def fechas_int(self, x):
        try:
            return int(x)
        except:
            return 0


if __name__ == "__main__":
    dt = recomendador_categoria()
    print(dt.obtener_recomendaciones('genre','["action","adventure"]'))
