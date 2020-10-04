# Dependencias
import pandas as pd
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import random
# %matplotlib inline


class recomendador_calificaciones:
    movies_data_chunk = pd.DataFrame()
    movies_df = pd.read_csv('src/ratings/movies_metadata.csv', low_memory=False, encoding='unicode_escape')
    ratings_df = pd.read_csv('src/ratings/ratings.csv', low_memory=False, encoding='unicode_escape')
    movies_category_data = pd.read_csv('src/categories/categories_metadata.csv', low_memory=False, encoding='unicode_escape')

    def __init__(self):
        # Limpieza del dataframe Movies
        # Creando la columna años
        self.movies_df['year'] = self.movies_df.title.str.extract(r'(\d\d\d\d)',expand=False)
        # Extraer los años de la columna de películas
        self.movies_df['title'] = self.movies_df.title.astype(str).str.replace(r'\([^)]*\)', '').str.strip()
        # # Eliminar la columna géneros
        # self.movies_df = self.movies_df.drop('genres', 1)

        # Limpieza del dataframe Ratings
        self.ratings_df = self.ratings_df.drop('timestamp', 1)


    def user_input(self, userInput):
        inputMovies = pd.DataFrame(userInput)
        # Filtrar las películas por título
        inputId = self.movies_df[self.movies_df['title'].isin(inputMovies['title'].tolist())]
        # Luego juntarlas para obtener el movieId. Implícitamente, lo está uniendo por título.
        inputMovies = pd.merge(inputId, inputMovies)
        # Eliminando información que no utilizaremos del dataframe de entrada
        inputMovies = inputMovies.drop('year', 1)
        return inputMovies

    def obtener_recomendaciones(self, userInput, percentile=0.8):
        inputMovies = self.user_input(userInput)
        userSubset = self.ratings_df[self.ratings_df['movieId'].isin(inputMovies['movieId'].tolist())]

        userSubsetGroup = userSubset.groupby(['userId'])
        userSubsetGroup.get_group(1130)
        userSubsetGroup = sorted(userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)
        userSubsetGroup = userSubsetGroup[0:100]

        #Guardar la Correlación Pearson en un diccionario
        pearsonCorrelationDict = {}
        for name, group in userSubsetGroup:
            #Comencemos ordenando el usuario actual y el ingresado de forma tal que los valores no se mezclen luego
            group = group.sort_values(by='movieId')
            inputMovies = inputMovies.sort_values(by='movieId')
            #Obtener el N para la fórmula
            nRatings = len(group)
            #Obtener los puntajes de revisión para las películas en común
            temp_df = inputMovies[inputMovies['movieId'].isin(group['movieId'].tolist())]
            #Guardarlas en una variable temporal con formato de lista para facilitar cálculos futuros
            tempRatingList = temp_df['rating'].tolist()
            #Pongamos también las revisiones de grupos de usuarios en una lista
            tempGroupList = group['rating'].tolist()
            #Calculemos la Correlación Pearson entre dos usuarios, x e y
            Sxx = sum([i**2 for i in tempRatingList]) - pow(sum(tempRatingList),2)/float(nRatings)
            Syy = sum([i**2 for i in tempGroupList]) - pow(sum(tempGroupList),2)/float(nRatings)
            Sxy = sum( i*j for i, j in zip(tempRatingList, tempGroupList)) - sum(tempRatingList)*sum(tempGroupList)/float(nRatings)

            #Si el denominador es diferente a cero, entonces dividir, sino, la correlación es 0.
            if Sxx != 0 and Syy != 0:
                pearsonCorrelationDict[name] = Sxy/sqrt(Sxx*Syy)
            else:
                pearsonCorrelationDict[name] = 0

        pearsonCorrelationDict.items()

        pearsonDF = pd.DataFrame.from_dict(pearsonCorrelationDict, orient='index')
        pearsonDF.columns = ['similarityIndex']
        pearsonDF['userId'] = pearsonDF.index
        pearsonDF.index = range(len(pearsonDF))

        topUsers=pearsonDF.sort_values(by='similarityIndex', ascending=False)[0:50]
        topUsersRating=topUsers.merge(self.ratings_df, left_on='userId', right_on='userId', how='inner')
        topUsersRating['weightedRating'] = topUsersRating['similarityIndex']*topUsersRating['rating']

        tempTopUsersRating = topUsersRating.groupby('movieId').sum()[['similarityIndex','weightedRating']]
        tempTopUsersRating.columns = ['sum_similarityIndex','sum_weightedRating']
        #Se crea un dataframe vacío
        recommendation_df = pd.DataFrame()
        #Ahora se toma el promedio ponderado
        recommendation_df['weighted average recommendation score'] = tempTopUsersRating['sum_weightedRating']/tempTopUsersRating['sum_similarityIndex']
        recommendation_df['movieId'] = tempTopUsersRating.index
        recommendation_df = recommendation_df.sort_values(by='weighted average recommendation score', ascending=False)
        
        recommendation = self.movies_df.loc[self.movies_df['movieId'].isin(recommendation_df['movieId'].tolist())]
        movies_data = self.movies_category_data[self.movies_category_data['title'].isin(recommendation['title'].tolist())]
        movies_data = movies_data.dropna(axis=0,how='any')
        recMovies = pd.concat([movies_data, recommendation],axis=0)
        recMovies = recMovies.drop('movieId',axis=1)
        recMovies = recMovies.dropna(axis=0,how='any')
        recMovies = recMovies.drop_duplicates(subset=['title'])

        # Aleatorios
        rndm_count = int(random.uniform(1,120))
        rndm=int(random.uniform(1,len(recMovies)))
        start = 1 
        end = 1
        if((rndm+rndm_count) > len(recMovies)):
            start = rndm - rndm_count
            end = rndm
        elif((rndm-rndm_count)<0):
            start = rndm
            end = rndm+rndm_count
        else:
            start = rndm
            end = rndm+rndm_count

        recMovies = recMovies[start:end]

        # SCORES
        C = recMovies['vote_average'].mean()
        m = recMovies['vote_count'].quantile(percentile)
        recMovies = recMovies.copy().loc[recMovies['vote_count'] >= m]
        
        # Calcular el score usando la forumal de IMDB
        recMovies['score'] = recMovies.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average'])+ (m/(m+x['vote_count']) * C), axis=1)


        print('\n\nRespuesta')
        return recMovies.sort_values('score',ascending=False).to_dict('records')

if __name__ == "__main__":
    dt = recomendador_calificaciones()
    userInput = [
                    # {'title':'Breakfast Club, The', 'rating':5},
                    {'title':'Toy Story', 'rating':3.5},
                    {'title':'Jumanji', 'rating':2},
                    {'title':"Pulp Fiction", 'rating':5},
                    {'title':'Akira', 'rating':4.5}
                ] 
    print(dt.obtener_recomendaciones(userInput))