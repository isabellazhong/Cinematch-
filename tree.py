import csv

class Movie:

    """The class for the movie, which will be a node in the 
        decision tree when choosing a movie to watch for the user

        Instance Attributes:
            - genre: the genre of the novie 
            - duration: how long the movie is in minutes
            - rating: the rotton tomatoes the movie has 
    """

    genre: str
    duration: float
    rating: int 


class MovieTree:
    
    """This class is a decision tree to filter out 
        movies for the user to watch 
    """

    _root: Movie
    _subtrees: list[Movie]