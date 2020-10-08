# DEPENDENCIAS
import pandas as pd
import numpy as np
from os import path
import pickle, json
from ast import literal_eval
import random


# CLASE CONTROLADOR DE RECOMENDADOR POR CATEGORIAS
class categoriesController:
    # VARIABLES PRINCIPALES
    # DataFrame desde el CSV con tratamiento de datos
    movies_metadata = pd.read_csv('src/categories/movies_metadata.csv', low_memory=False, encoding='unicode_escape')
    # Variable vacía para el resultado del DataFrame
    movies_df = None

    # Constructor
    def __init__(self):
        # CREACIÓN DEL DATAFRAME EN EL CONSTRUCTOR DE LA CLASE
        # Si el archivo CSV de los datos tratados existe, se hace la lectura
        if(path.exists('src/categories/categories_metadata.csv')):
            self.movies_df = pd.read_csv('src/categories/categories_metadata.csv', low_memory=False, encoding='unicode_escape')
        # Si el archivo CSV de los datos tratados no existe, se construye y se hace la lectura
        else:
            # Se preparan las columnas a utilizar de todo el CSV
            cols = self.movies_metadata.columns
            self.movies_metadata = self.movies_metadata[['title', 'genres', 'release_date','runtime', 'vote_average', 'vote_count']]

            # Conversión de fechas a formato admitido por Pandas
            self.movies_metadata['release_date'] = pd.to_datetime(self.movies_metadata['release_date'], errors='coerce')

            # Agregar columna year al dataframe
            self.movies_metadata['year'] = self.movies_metadata['release_date'].apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
            # Solución a los valores NaT en las fechas de la columna release_date
            self.movies_metadata['year'] = self.movies_metadata['year'].apply(self.fechas_int)

            # Eliminar columna release_date
            self.movies_metadata = self.movies_metadata.drop('release_date', axis=1)

            # Se prepara la columna 'genres' para convertir el string en un objeto(diccionario)
            self.movies_metadata['genres'] = self.movies_metadata['genres'].fillna('[]')
            self.movies_metadata['genres'] = self.movies_metadata['genres'].apply(literal_eval)
            self.movies_metadata['genres'] = self.movies_metadata['genres'].apply(lambda x: [i['name'].lower() for i in x] if isinstance(x, list) else [])

            # Ajuste de la categoría géneros del DataFrame
            s = self.movies_metadata.apply(lambda x: pd.Series(x['genres']), axis=1).stack().reset_index(level=1, drop=True)
            s.name = 'genre'
            self.movies_df = self.movies_metadata.drop('genres', axis=1).join(s)
            self.movies_df.to_csv('src/categories/categories_metadata.csv',index=False)


    # FUNCIÓN PARA LA OBTENCIÓN DE RECOMENDACIONES POR CATEGORÍAS, PARÁMETROS SOLICITADOS:
    # feature: columna del DataFrame (Para este caso se usa 'genres')
    # params: lista de categorías seleccionadas desde la vista
    def obtener_recomendaciones(self, feature, params, percentile=0.8):
        # VARIABLES PARA OPERACIÓN
        feature = feature 
        genres_list = params
        movies_list = pd.Series([],dtype=pd.StringDtype())

        # Recorrer los géneros para la construcción la lista
        for i in genres_list:
            # Se hace una copia del DataFrame con los datos tratados
            movies = self.movies_df.copy()
            movies = movies[(movies[feature] == i) ]
            # Eliminar las filas que contengan alguna columna vacía
            movies = movies.dropna(axis=0,how='any')

            # Si el DataFrame no está vacío
            if(movies.empty != True):
                # Creación de variables para calcular el score mediante la fórmula de IMDB
                C = movies['vote_average'].mean()
                m = movies['vote_count'].quantile(percentile)
                q_movies = movies.copy().loc[movies['vote_count'] >= m]
                
                # Calcular el score usando la formula de IMDB
                q_movies['score'] = q_movies.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average'])+ (m/(m+x['vote_count']) * C), axis=1)
                
                # SELECCIÓN DE ALEATORIOS PARA LA RECOMENDACIÓN
                rndm_count = int(random.uniform(1,40))
                rndm=int(random.uniform(1,len(q_movies)))
                start = 1 
                end = 1
                if((rndm+rndm_count) > len(q_movies)):
                    start = rndm - rndm_count
                    end = rndm
                elif((rndm-rndm_count)<0):
                    start = rndm
                    end = rndm+rndm_count
                else:
                    start = rndm
                    end = rndm+rndm_count

                q_movies = q_movies[start:end]

                # LA VARIABLE 'movies_list' SE CONCATENA CON LAS PÉLICULAS OBTENIDAS DURANTE LA SELECCIÓN ALEATORIA
                movies_list = pd.concat([movies_list,q_movies])
        
        # SE HACE LA LIMPIEZA DE COLUMNAS DUPLICADAS
        movies_list.drop(movies_list.columns[0], axis=1, inplace=True)
        movies_list.drop(movies_list.columns[0], axis=1, inplace=True)
        # LAS PELÍCULAS SE ORDENAN POR LA COLUMNA 'score'
        movies_list.sort_values('score',ascending=False)
        # SE ELIMINAN LAS FILAS QUE SE REPITEN EN LA COLUMNA 'title'
        movies_list = movies_list.drop_duplicates(subset=['title'])
        
        # RETORNA LA LISTA ORDENADA POR LA COLUMNA 'score' EN FORMA DE DICCIONARIO (SOLO LOS REGISTROS)
        return movies_list.sort_values('score',ascending=False).to_dict('records')

    # Función de apoyo al tratamiento de fechas en el dataframe
    # FUNCIÖN DE APOYO AL TRATAMIENTO DE LAS FECHAS DEL DATAFRAME
    def fechas_int(self, x):
        try:
            return int(x)
        except:
            return 0

# CONSTRUCTOR PARA PRUEBAS CON DATOS PRECARGADOS
if __name__ == "__main__":
    dt = recomendador_categoria()
    print(dt.obtener_recomendaciones('genre','["action","adventure"]'))
