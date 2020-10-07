# Dependencias
import pandas as pd
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import random
from os import path
# %matplotlib inline


class ratingsController:
    movies_df = pd.read_csv('src/ratings/movies.csv', low_memory=False, encoding='unicode_escape')
    ratings_df = pd.read_csv('src/ratings/ratings.csv', low_memory=False, encoding='unicode_escape')
    movies_category_data = pd.read_csv('src/categories/movies_metadata.csv', low_memory=False, encoding='unicode_escape')

    def __init__(self):
        # Si existe el archivo dataset se asigna el valor a la variable global
        if(path.exists('src/ratings/movies_dataset.csv')):
            print('EXISTE DATASET')
            self.movies_df = pd.read_csv('src/ratings/movies_dataset.csv', low_memory=False, encoding='unicode_escape')
            self.ratings_df = self.ratings_df.drop('timestamp',axis=1)
        # De lo contrario, lo construye a partir de los archivos de dataset correspondientes
        else:
            print('NO EXISTE DATASET')
            # Adecuando el catálogo de peliculas del recomendador por calificaciones
            self.movies_df['year'] = self.movies_df.title.str.extract(r'(\d\d\d\d)',expand=False)
            # Extraer los años de la columna de películas
            self.movies_df['title'] = self.movies_df.title.astype(str).str.replace(r'\([^)]*\)', '').str.strip()
            self.movies_df = self.movies_df.drop('genres',axis=1)
            
            # Adecuando los títulos de las películas en el catálodo del recomendador por calificaciones
            for i, row in enumerate(self.movies_df['title']):
                val = row
                if ', The' in val:
                    val = row.split(', ')[1]+' '+row.split(', ')[0]
                elif ', Le' in val:
                    val = row.split(', ')[1]+' '+row.split(', ')[0]
                elif ', L\'' in val:
                    val = row.split(', ')[1]+' '+row.split(', ')[0]
                elif ', El' in val:
                    val = row.split(', ')[1]+' '+row.split(', ')[0]
                elif ', A' in val:
                    val = row.split(', ')[1]+' '+row.split(', ')[0]
                elif ', An' in val:
                    val = row.split(', ')[1]+' '+row.split(', ')[0]
                
                self.movies_df.at[i,'title'] = val

            print('Movies DF size: '+str(len(self.movies_df)))

            # Leyendo los datos del catálogo de peliculas del recomendador por categorías
            self.movies_category_data = self.movies_category_data[['title', 'release_date','runtime', 'vote_average', 'vote_count']]
            self.movies_category_data['release_date'] = pd.to_datetime(self.movies_category_data['release_date'], errors='coerce')
            self.movies_category_data = self.movies_category_data.rename(columns={'release_date':'year'})
            print('Movies CAT size: '+str(len(self.movies_category_data)))

            movies_data = self.movies_category_data[self.movies_category_data['title'].isin(self.movies_df['title'].tolist())]
            print('Movies MOVIES_DATA size: '+str(len(movies_data)))

            # Mezclando los datos del catálogo de películas del recomendador por calificaciones con los del recomendador por categorías
            recMovies = movies_data.merge(self.movies_df, on='title',how="left").drop('year_y',axis=1)
            recMovies[['runtime']] = recMovies[['runtime']].fillna(0)
            recMovies = recMovies.dropna(axis=0,how='any').rename(columns={'year_x':'year'})

            print('Movies MIX size: '+str(len(recMovies)))
            
            # Calcular el score usando la forumal de IMDB
            C = recMovies['vote_average'].mean()
            m = recMovies['vote_count'].quantile(0.8)
            # recMovies = recMovies.copy().loc[recMovies['vote_count'] >= m]
            recMovies['score'] = recMovies.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average'])+ (m/(m+x['vote_count']) * C), axis=1)
            recMovies = recMovies.sort_values(by=['title'])

            print('Movies SCORE size: '+str(len(recMovies)))
            
            
            recMovies = recMovies.drop_duplicates(subset=['title','year'])
            print('Movies REMOVE_DUPLICATES size: '+str(len(recMovies)))
            
            recMovies.to_csv('src/ratings/movies_dataset.csv',index=False)

            self.movies_df = pd.read_csv('src/ratings/movies_dataset.csv', low_memory=False, encoding='unicode_escape')
            self.ratings_df = self.ratings_df.drop('timestamp',axis=1)

            


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
        userSubsetGroup = sorted(userSubsetGroup,  key=lambda x: len(x[1]), reverse=True)
        userSubsetGroup = userSubsetGroup[0:100]

        #Guardar la Correlación Pearson en un diccionario
        pearsonCorrelationDict = {}
        for name, group in userSubsetGroup:
            #Comencemos ordenando el usuario actual y el ingresado de forma tal que los valores no se mezclen luego
            group = group.sort_values(by='movieId')
            inputMovies = inputMovies.sort_values(by='movieId')
            inputMovies['rating'] = inputMovies['rating'].astype(float)
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
        
        recMovies = self.movies_df.loc[self.movies_df['movieId'].isin(recommendation_df['movieId'].tolist())]

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

        return recMovies.drop('movieId',axis=1).to_dict('records')

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