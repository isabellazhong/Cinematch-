"""
Module Description
==================

This is the main module for PickMeWatchMe, a movie recommedation system that reccomends
users movies based on inputted actors, genres, etc. 

This module runs a Tkinter-based graphical user interface and uses the recommender module to allow user input

Copyright and Usage Information
===============================

This file is solely for the personal and private use of 
Victoria Cai, Isabella Zhong, Maya Dowman, Grace-Keyi Wang. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2025 Victoria Cai, Isabella Zhong, Maya Dowman, Grace-Keyi Wang
"""
import tkinter as tk
from tkinter import ttk
<<<<<<< HEAD
import csv
from tree import MovieDecisionTree
from tree import BinaryCSV
from Recommender import Recommender


# Configure styles
style = ttk.Style()
style.theme_use('clam')
style.configure('Dark.TFrame', background='#2A2A2A')
style.configure('Accent.TButton', font=('Arial', 14),
                foreground='white', background='#4ECDC4')
style.configure('Secondary.TButton', font=('Arial', 14),
                foreground='white', background='#FF6B6B')
=======
from recommender import Recommender
>>>>>>> 11277959fa956fbf4fe7340915b9463002232f6f


if __name__ == "__main__":

<<<<<<< HEAD
#     # import doctest
#     #
#     # doctest.testmod()
#     #
#     # import python_ta
#     #
#     # python_ta.check_all(config={
#     #     'max-line-length': 120,
#     #     'disable': ['E1136'],
#     #     'extra-imports': ['csv', 'networkx'],
#     #     'allowed-io': ['load_movie_actor_graph'],
#     #     'max-nested-blocks': 4
#     # })
    BinaryCSV('imdb_top_1000.csv', 'decision_tree.csv').create_decision_csv()
    
=======
    import python_ta.contracts
    python_ta.contracts.check_all_contracts()
>>>>>>> 11277959fa956fbf4fe7340915b9463002232f6f

    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['tkinter', 'recommender'],
        'max-nested-blocks': 4
    })

    # Configure styles
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Dark.TFrame', background='#2A2A2A')
    style.configure('Accent.TButton', font=('Arial', 14), foreground='white', background='#4ECDC4')
    style.configure('Secondary.TButton', font=('Arial', 14), foreground='white', background='#FF6B6B')

    # Initialize and run recommender
    root1 = tk.Tk()
    app = Recommender(root1)
    root1.mainloop()
