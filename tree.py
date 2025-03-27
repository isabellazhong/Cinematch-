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
    def transform_movie_data(self, movie_file:str):
        movies = MovieData.load_movie_basics(movie_file)
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
        df['runtime'] =  df['runtime'].str.extract(r'(\d+)').astype(float)
        df['genre'] = df['genre'].str.split(', ')
        df_explode_genre = df.explode('genre')
        df_onehot_genre = pd.get_dummies(df_explode_genre, columns=['genre'], dtype=int)
        df2 = df_onehot_genre.groupby('title', as_index=False).sum()

      
        runtime_intervals = [0, 60, 90, 120, 180, 240, np.inf]
        runtime_labels = ['very-short', 'short', 'mid', 'mid-long', 'long', 'very-long']
        df2['runtime_bin'] = pd.cut(df2['runtime'], bins=runtime_intervals, labels=runtime_labels)
        
        df_explode_runtime = df2.explode('runtime_bin')
        df_onehot_runtime = pd.get_dummies(df_explode_runtime, columns=['runtime_bin'], dtype=int)
        df_final = df_onehot_runtime.groupby('title', as_index=False).sum()
        return df_final

    #creates a csv of a pathway for each movie that the tree can pass through
    def create_decision_csv(self, movie_file:str, decision_file:str):
        df = self.transform_movie_data(movie_file)
        genre_columns = [col for col in df.columns if col.startswith('genre_')]
        runtime_columns = [col for col in df.columns if col.startswith('runtime_bin_')]
        df = df[['title'] + runtime_columns + genre_columns]
        df.to_csv(decision_file, encoding='utf-8', index=False)
        

    # def get_user_input(question: list, input:list):

        

y = MovieDecisionTree()
# print(y.transform_movie_data('movie_data_small.csv'))
y.create_decision_csv('imdb_top_1000.csv', 'decision_tree.csv')
   












    

