"""CSC111 Winter 2025 Exercise 4: More Graphs and Recommendations (Part 1)

Module Description
==================
This module implements the decision tree to reccomend a movie for the user. 

For Movie class:
- Creates a node for the movie (the leaves of the tree)

For the BinaryCSV:
- Transforms the orginal mvoie dataset into a binary one so that the tree can be traversed through
- Uses one-hot encoding to transform the categories

For MovieDecisionTree:
- Includes methods to create the tree and to traverse through 

Copyright and Usage Information
===============================

This file is solely for the personal and private use of 
Victoria Cai, Isabella Zhong, Maya Dowman, Grace-Keyi Wang. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2025 Victoria Cai, Isabella Zhong, Maya Dowman, Grace-Keyi Wang
"""
from typing import Any, Optional
import pickle
import pandas as pd
import numpy as np
from movie_data import MovieData


class Movie:

    """The class for the movie, which will be a end node in the
        decision tree when choosing a movie to watch for the user

        Instance Attributes:
            - self.title: the title of the movie
            - self.genre: the genre of the novie
            - self.duration: how long the movie is in minutes
            - self.rating: the rotton tomatoes the movie has
    """

    title: str
    link: str
    duration: float
    rating: float

    def __init__(self, title: str, link: str, duration: float, rating: float) -> None:
        self.title = title
        self.link = link
        self.duration = duration
        self.rating = rating


class BinaryCSV:
    """
        Turns the data in the movie csv into a hot-encoded one (binary data) 

        Instance Attributes:
            - self.movie_file: the movie csv file 
            - self.decision_file: csv file to put the binary data in 
        
    """
    movie_file: str
    decision_file: str

    def __init__(self, m_file: str, d_file: str) -> None:
        """
            initializes the binary_csv instance attributes
        """
        self.movie_file = m_file
        self.decision_file = d_file

    def encode(self, key: str, df: pd.DataFrame) -> pd.DataFrame:
        """
           hot one encodes data of a specific column
        """
        df_explode = df.explode(key)
        df_onehot = pd.get_dummies(df_explode, columns=[key], dtype=int)
        return df_onehot

    def get_data(self) -> list:
        """
            processes the data in the movie csv file and returns it as a list
        """
        movies = MovieData.load_movie_basics(self.movie_file)
        movie_object_index = 1

        data = []
        for movie in movies.items():
            movie_data = movie[movie_object_index]
            poster_link, series_title = movie_data.poster_title
            genres, runtime = movie_data.genre_runtime
            overview, imdb_rating = movie_data.overview_rating

            # data for the dataframe
            data.append({
                "title": series_title,
                "poster": poster_link,
                "genre": genres if genres else np.nan,
                "runtime": runtime,
                "overview": overview,
                "imdb_rating": float(imdb_rating) if imdb_rating else np.nan,
                # serialize the movie node so that it can be formmated in the csv as a string
                "movie_node": pickle.dumps(Movie(series_title, poster_link, runtime, imdb_rating))
            })
        return data

    def transform_movie_data(self) -> pd.DataFrame:
        """
            uses one hot encoder to convert to numerical data, returns data frame
        """
        # #adjusts data type
        df = pd.DataFrame(self.get_data())
        df['runtime'] = df['runtime'].str.extract(r'(\d+)').astype(float)
        df['genre'] = df['genre'].str.split(', ')

        runtime_intervals = [0, 60, 90, 120, 180, 240, np.inf]
        runtime_labels = ['very-short', 'short', 'mid', 'mid-long', 'long', 'very-long']
        df['runtime_bin'] = pd.cut(df['runtime'], bins=runtime_intervals, labels=runtime_labels)
        df_final = self.encode('runtime_bin', df)
        df_final = self.encode('genre', df_final)

        df_final = df_final.groupby('title', as_index=False).max()
        return df_final

    def create_decision_csv(self) -> None:
        """
            creates a csv of a pathway for each movie that the tree can pass through
        """
        df = self.transform_movie_data()
        genre_columns = [col for col in df.columns if col.startswith('genre_')]
        runtime_columns = [col for col in df.columns if col.startswith('runtime_bin_')]
        df = df[['movie_node'] + runtime_columns + genre_columns]
        df.to_csv(self.decision_file, encoding='utf-8', index=False)


class MovieDecisionTree:

    """This class is a decision tree to filter out
        movies for the user to watch

        Instance attributes:
            - self._root: the root of the decision tree
            - self._subtrees: the subtrees of the tree 
    """
    _root: Optional[Any]
    _subtrees: list[Any]

    def __init__(self, root: Optional[Any], subtrees: list[Any]) -> None:
        """
            initializes the moviedecisiontree instance attributes
        """
        self._root = root
        self._subtrees = subtrees

    def is_empty(self) -> bool:
        """
            checks if tree empty
        """
        return self._root is None

    def get_root(self) -> Any:
        """
            gets the root of the tree
        """
        return self._root

    def get_subtrees(self) -> list:
        """
            gets the subtrees of the tree
        """
        return self._subtrees

    def traverse_tree(self, inputs: list) -> Any:
        """
            traverses the tree with user_input, returns not found if the branch doesn't exist
        """
        if self.is_empty():
            return []
        elif not inputs:
            if not self._subtrees:
                return []
            else:
                return [s._root for s in self._subtrees]
        else:
            for subtree in self._subtrees:
                if subtree.get_root() == str(inputs[0]):
                    return subtree.traverse_tree(inputs[1:])
        return "Not Found"

    def create_branch(self, lst: list) -> None:
        """
            Creates a branch for the tree
        """
        if not lst:
            return None
        else:
            for subtree in self._subtrees:
                if lst[0] == subtree.get_root():
                    subtree.create_branch(lst[1:])
                    return

            new_tree = MovieDecisionTree(lst[0], [])
            self._subtrees.append(new_tree)
            new_tree.create_branch(lst[1:])

    def go_left_most(self) -> Movie:
        """
            Goes to leftmost branch
        """
        if self._root is None:
            return None
        elif not self._subtrees:
            return self._root
        else:
            left = self._subtrees[0]
            return left.go_left_most()

    def go_right_most(self) -> Movie:
        """
            goes to right most branch
        """
        if self._root is None:
            return None
        elif not self._subtrees:
            return self._root
        else:
            left = self._subtrees[-1]
            return left.go_right_most()

    def get_movies(self) -> list[Movie]:
        """
            returns list of ALL movies at a subtree in the main tree
        """
        movies = []

        if not self.get_root() or not self.get_subtrees():
            return []
        seen_movies = set()

        for subtree in self.get_subtrees():
            right = subtree.go_right_most()
            left = subtree.go_left_most()

            if right is not None and right not in seen_movies:
                movies.append(right)
                seen_movies.add(right)

            if left is not None and left not in seen_movies:
                movies.append(left)
                seen_movies.add(left)

        return movies

    # #returns all movies that have the same input up to a specific depth of a tree
    # def movie_up_to_depth(self, input: list, depth_index: int) -> list[Movie]:
    #     MAX_DEPTH = 27
    #     if depth_index > MAX_DEPTH:
    #         return []
    #     # Traverse the tree up to the specific depth
    #     trees = self.traverse_tree(input[:depth_index])
    #     movies = []
    #     if len(trees) > 1:
    #         for tree in trees:
    #             movies.extend(tree.get_movies())
    #     else:
    #         movies = tree.get_movies()
    #     return movies


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['movie_data', 'numpy', 'pandas', 'pickle'],  # the names (strs) of imported modules
        'allowed-io': [],     # the names (strs) of functions that call print/open/input
        'max-line-length': 120
    })
