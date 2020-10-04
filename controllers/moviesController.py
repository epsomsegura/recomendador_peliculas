import pandas as pd
from os import path


class moviesController:
    movies_df = pd.read_csv('src/ratings/movies.csv', low_memory=False, encoding='unicode_escape')
    movies_category_data = pd.read_csv('src/categories/categories_metadata.csv', low_memory=False, encoding='unicode_escape')
    movies_data = None

    # Constructor
    def __init__(self):
            recMovies.to_csv('src/ratings/movies_metadata.csv',index=False)
    
    def getAll(self):
        recMovies = None
        # Creación del dataFrame en el constructor
        if(path.exists('src/ratings/movies_metadata.csv')):
            recMovies= pd.read_csv('src/ratings/movies_metadata.csv', low_memory=False, encoding='unicode_escape')
        else:

            self.movies_df['year'] = self.movies_df.title.str.extract(r'(\d\d\d\d)',expand=False)
            self.movies_df['title'] = self.movies_df.title.astype(str).str.replace(r'\([^)]*\)', '').str.strip()

            for i, row in self.movies_df.iterrows():
                value = row.title
                if ', The' in row.title:
                    value = row.title.split(', ')[1]+' '+row.title.split(', ')[0]

                self.movies_df.at[i,'title'] = value
            self.movies_df = self.movies_df.drop('genres', 1)

            movies_category = self.movies_category_data[self.movies_category_data['title'].isin(self.movies_df['title'].tolist())]
            movies_category = movies_category.dropna(axis=0,how='any')
            recMovies = pd.concat([movies_category, self.movies_df],axis=0)
            recMovies = recMovies.drop('movieId',axis=1)
            recMovies = recMovies.dropna(axis=0,how='any')
            recMovies = recMovies.drop_duplicates(subset=['title'])
        
        return recMovies.sort_values('year',ascending=False).to_dict('records')


if __name__ == '__main__':
    x = moviesController()
    x.getAll()