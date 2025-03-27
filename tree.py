import csv
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from MovieData import MovieData

class Movie:

    """The class for the movie, which will be a node in the
        decision tree when choosing a movie to watch for the user

        Instance Attributes:
            - title: the title of the movie
            - genre: the genre of the novie
            - duration: how long the movie is in minutes
            - rating: the rotton tomatoes the movie has
    """

    title: str
    genre: str
    duration: float
    rating: int


class MovieDecisionTree:

    """This class is a decision tree to filter out
        movies for the user to watch
    """
    def __init__(self):
        self.tree = None


    #uses one hot encoder to convert to numerical data
    def transform_movie_data(self, file:str):
        movies = MovieData.load_movie_basics(file)
        data = []
        MOVIE_OBJECT_INDEX = 1

        for movie in movies.items():
            movie_data = movie[MOVIE_OBJECT_INDEX]
            poster_link, series_title = movie_data.poster_title
            genres, runtime = movie_data.genre_runtime
            overview, imdb_rating = movie_data.overview_rating

            data.append({
                "title": series_title,
                "poster": poster_link,
                "genre": genres if genres else np.nan,
                "runtime": runtime,
                "overview": overview,
                "imdb_rating": float(imdb_rating) if imdb_rating else np.nan 
            })


        # #adjusts data type 
        df = pd.DataFrame(data)
        df['runtime'] =  df['runtime'].str.extract('(\d+)').astype(float)
        df['genre'] = df['genre'].str.split(', ')
        df_explode_genre = df.explode('genre')
        df_onehot = pd.get_dummies(df_explode_genre, columns=['genre'], dtype=int)
        df_final = df_onehot.groupby('title', as_index=False).sum()

      
        runtime_intervals = [0, 60, 90, 120, 180, 240, np.inf]
        runtime_labels = [1,2,3,4,5,6]
        df_final['runtime_bin'] = pd.cut(df_final['runtime'], bins=runtime_intervals, labels=runtime_labels)

        return df_final 


y = MovieDecisionTree()
print(y.transform_movie_data('movie_data_small.csv'))







    

