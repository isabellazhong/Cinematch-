import csv
<<<<<<< HEAD
from typing import Optional
=======
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import tree
from MovieData import MovieData

>>>>>>> c7bba8c7725c8fb3756e4f103e418f56bcfac48b
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


<<<<<<< HEAD
class MovieTree:

    """This class is a decision tree to filter out 
        movies for the user to watch 
=======
class MovieDecisionTree:

    """This class is a decision tree to filter out
        movies for the user to watch
>>>>>>> c7bba8c7725c8fb3756e4f103e418f56bcfac48b
    """
    def __init__(self):
        self.tree = None

<<<<<<< HEAD
    _root: Optional[Any]
    _subtrees: list[MovieTree]
    
    #checks if tree is empty
    def is_empty(self):
        return self._root is None

    def add_node(self, node:)



=======

    def build_decision_tree(self):
        movies_dict = MovieData.load_movie_basics()
        features = []
        predicted_movies = []
        for movie in movies_dict:
            genre = movies_dict[movie].genre_runtime[0]
            runtime = movies_dict[movie].genre_runtime[1]
            rating = movies_dict[movie].overview_rating[1]

            #convert the categorical genres to values
>>>>>>> c7bba8c7725c8fb3756e4f103e418f56bcfac48b
