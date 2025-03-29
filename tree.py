import csv
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from MovieData import MovieData
from typing import Any, Optional

class Movie:

    """The class for the movie, which will be a end node in the
        decision tree when choosing a movie to watch for the user

        Instance Attributes:
            - title: the title of the movie
            - genre: the genre of the novie
            - duration: how long the movie is in minutes
            - rating: the rotton tomatoes the movie has
    """

    title: str
    link: str
    genre: str
    duration: float
    rating: int

    def __init__(self, title, link, genre, duration, rating):
        self.title = title
        self.link = link
        self.genre = genre
        self.duration = duration
        self.rating = rating

    #turns the class into a string to store in csv
    def __repr__(self) -> str:
        return f"Movie('{self.title}', '{self.link}', '{self.genre}', '{self.duration}', '{self.rating}')"


class Binary_Csv:
    movie_file: str
    decision_file: str


    def __init__(self, m_file, d_file):
        self.movie_file = m_file
        self.decision_file = d_file


    # hot one encodes data of a specific column
    def encode(self, key: str, df: pd.DataFrame):
        df_explode = df.explode(key)
        df_onehot = pd.get_dummies(df_explode, columns=[key], dtype=int)
        return df_onehot


    #uses one hot encoder to convert to numerical data
    def transform_movie_data(self):
        movies = MovieData.load_movie_basics(self.movie_file)
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
                "imdb_rating": float(imdb_rating) if imdb_rating else np.nan,
                "movie_node": Movie(series_title, poster_link, genres, runtime, imdb_rating).__repr__()
            })


        # #adjusts data type
        df = pd.DataFrame(data)
        df['runtime'] =  df['runtime'].str.extract(r'(\d+)').astype(float)
        df['genre'] = df['genre'].str.split(', ')

        runtime_intervals = [0, 60, 90, 120, 180, 240, np.inf]
        runtime_labels = ['very-short', 'short', 'mid', 'mid-long', 'long', 'very-long']
        df['runtime_bin'] = pd.cut(df['runtime'], bins=runtime_intervals, labels=runtime_labels)
        df_final = self.encode('runtime_bin', df)
        df_final = self.encode('genre', df_final)

        df_final = df_final.groupby('title', as_index=False).max()
        return df_final

    #creates a csv of a pathway for each movie that the tree can pass through
    def create_decision_csv(self):
        df = self.transform_movie_data()
        genre_columns = [col for col in df.columns if col.startswith('genre_')]
        runtime_columns = [col for col in df.columns if col.startswith('runtime_bin_')]
        df = df[['movie_node'] +  runtime_columns + genre_columns]
        df.to_csv(self.decision_file, encoding='utf-8', index=False)


class MovieDecisionTree:

    """This class is a decision tree to filter out
        movies for the user to watch
    """
    _root: Optional[Any]
    _subtrees: list[Any]

    def __init__(self, root: Optional[Any], subtrees: list[Any]):
        self._root = root
        self._subtrees = subtrees

    def is_empty(self):
        return self._root is None

    def get_root(self):
        return self._root

    def get_subtrees(self):
        return self._subtrees

    #traverses the tree with user_input
    def traverse_tree(self, inputs: list):

        if self.is_empty():
            return []
        elif not inputs:
            if not self._subtrees:
                return []
            else:
                return [tree.get_root() for tree in self._subtrees]
        else:
            for subtree in self._subtrees:
                if subtree.get_root() == inputs[0]:
                    return subtree.traverse_tree(inputs[1:])
        raise KeyError

     #creates a branch for the tree
    def create_branch(self, lst: list):
        if not lst:
            pass
        else:
            for subtree in self._subtrees:
                if lst[0] == subtree.get_root():
                    self.create_branch(lst[1:])
                    return

            new_tree = MovieDecisionTree(lst[0], [])
            self._subtrees.append(new_tree)
            new_tree.create_branch(lst[1:])

    #goes to leftmost branch
    def go_left_most(self):
        if self._root is None:
            return
        elif not self._subtrees:
            return self._root
        else:
            left = self._subtrees[0]
            return left.go_left_most()

    #goes to right most branch
    def go_right_most(self):
        if self._root is None:
            return
        elif not self._subtrees:
            return self._root
        else:
            left = self._subtrees[-1]
            return left.go_right_most()

    #returns all movies that have the same input up to a specific depth of a tree
    def movie_up_to_depth(self, input: list, depth_index:int):
        MAX_DEPTH = 27
        if depth_index >= MAX_DEPTH:
            return []
        else:
            tree = self.traverse_tree(input[:depth_index])

            if not tree:
                return []
            elif not tree.get_subtrees():
                return []
            else:
                movies = []
                for subtree in tree.get_subtrees():
                    right = subtree.go_right_most()
                    left = subtree.go_left_most()

                    if right is not None:
                        movies.append(right)
                    if left is not None:
                        movies.append(left)

                return movies


y = Binary_Csv('imdb_top_1000.csv', 'decision_tree.csv')
# print(y.transform_movie_data('movie_data_small.csv'))
y.create_decision_csv()
