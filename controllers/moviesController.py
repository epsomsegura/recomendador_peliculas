# DEPENDENCIAS
import pandas as pd
from os import path

# CLASE CONTROLADOR DE PELÍCULAS
class moviesController:
    # VARIABLES PRINCIPALES
    movies_data = None
    movies_df = pd.read_csv('src/ratings/movies.csv', low_memory=False, encoding='unicode_escape')
    movies_category_data = pd.read_csv('src/categories/categories_metadata.csv', low_memory=False, encoding='unicode_escape')

    # Constructor
    def __init__(self):
        # Si existe el archivo dataset se asigna el valor a la variable global
        if(path.exists('src/ratings/movies_dataset.csv')):
            self.movies_df = pd.read_csv('src/ratings/movies_dataset.csv', low_memory=False, encoding='unicode_escape')
        # De lo contrario, lo construye a partir de los archivos de dataset correspondientes
        else:
            # Adecuando el catálogo de peliculas del recomendador por calificaciones
            self.movies_df['year'] = self.movies_df.title.str.extract(r'(\d\d\d\d)',expand=False)
            self.movies_df = self.movies_df.dropna(axis=0,how='any')
            # Extraer los años de la columna de películas
            self.movies_df['title'] = self.movies_df.title.astype(str).str.replace(r'\([^)]*\)', '').str.strip()
            self.movies_df = self.movies_df.drop('genres',axis=1)
            
            # Adecuando los títulos de las películas en el catálodo del recomendador por calificaciones
            for i, row in self.movies_df.iterrows():
                val = row['title']
                if ', The' in val:
                    val = row['title'].split(', ')[1]+' '+row['title'].split(', ')[0]
                elif ', Le' in val:
                    val = row['title'].split(', ')[1]+' '+row['title'].split(', ')[0]
                elif ', L\'' in val:
                    val = row['title'].split(', ')[1]+' '+row['title'].split(', ')[0]
                elif ', El' in val:
                    val = row['title'].split(', ')[1]+' '+row['title'].split(', ')[0]
                elif ', A' in val:
                    val = row['title'].split(', ')[1]+' '+row['title'].split(', ')[0]
                elif ', An' in val:
                    val = row['title'].split(', ')[1]+' '+row['title'].split(', ')[0]
                
                self.movies_df.loc[i,'title'] = val

            # Leyendo los datos del catálogo de peliculas del recomendador por categorías
            movies_data = self.movies_category_data[self.movies_category_data['title'].isin(self.movies_df['title'].tolist())]
            movies_data = movies_data.drop('genre',axis=1)
            movies_data = movies_data.drop_duplicates(subset=['title'])

            # Mezclando los datos del catálogo de películas del recomendador por calificaciones con los del recomendador por categorías
            recMovies = movies_data.merge(self.movies_df, on='title',how="left").drop('year_y',axis=1)
            recMovies[['runtime']] = recMovies[['runtime']].fillna(0)
            recMovies = recMovies.dropna(axis=0,how='any').rename(columns={'year_x':'year'})
            
            # Calcular el score usando la forumal de IMDB
            C = recMovies['vote_average'].mean()
            m = recMovies['vote_count'].quantile(0.8)
            recMovies = recMovies.copy().loc[recMovies['vote_count'] >= m]
            recMovies['score'] = recMovies.apply(lambda x: (x['vote_count']/(x['vote_count']+m) * x['vote_average'])+ (m/(m+x['vote_count']) * C), axis=1)
            
            recMovies.to_csv('src/ratings/movies_dataset.csv',index=False)

            self.movies_df = pd.read_csv('src/ratings/movies_dataset.csv', low_memory=False, encoding='unicode_escape')
            
    
    def getAll(self):
        recMovies = pd.read_csv('src/ratings/movies_dataset.csv', low_memory=False, encoding='unicode_escape')
        return recMovies.sort_values('year',ascending=False).to_dict('records')


if __name__ == '__main__':
    x = moviesController()
    print(x.getAll())