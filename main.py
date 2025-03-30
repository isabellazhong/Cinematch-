import tkinter as tk
from tkinter import ttk
import csv
from tree import MovieDecisionTree
from tree import Binary_Csv
from Recommender import Recommender


# Configure styles
style = ttk.Style()
style.theme_use('clam')
style.configure('Dark.TFrame', background='#2A2A2A')
style.configure('Accent.TButton', font=('Arial', 14),
                foreground='white', background='#4ECDC4')
style.configure('Secondary.TButton', font=('Arial', 14),
                foreground='white', background='#FF6B6B')


if __name__ == "__main__":
# # You can uncomment the following lines for code checking/debugging purposes.
#     # However, we recommend commenting out these lines when working with the large
#     # datasets, as checking representation invariants and preconditions greatly
#     # increases the running time of the functions/methods.
#     # import python_ta.contracts
#     # python_ta.contracts.check_all_contracts()

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
    Binary_Csv('imdb_top_1000.csv', 'decision_tree.csv').create_decision_csv()
    


    
    root1 = tk.Tk()
    app = Recommender(root1)
    root1.mainloop()

