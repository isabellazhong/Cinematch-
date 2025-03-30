import tkinter as tk
from tkinter import ttk
import csv
from tree import MovieDecisionTree
from tree import Binary_Csv
from Recommender import Recommender
import pickle


# Configure styles
style = ttk.Style()
style.theme_use('clam')
style.configure('Dark.TFrame', background='#2A2A2A')
style.configure('Accent.TButton', font=('Arial', 14),
                foreground='white', background='#4ECDC4')
style.configure('Secondary.TButton', font=('Arial', 14),
                foreground='white', background='#FF6B6B')

def build_decision_tree(file:str) -> MovieDecisionTree:
    tree = MovieDecisionTree('', [])
    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            movie = row[0]
            movie_list = row[1:] + [movie]
            tree.create_branch(movie_list)
    return tree

#encodes the user input into a binary list so that it can traversre through the list
def convert_user_input(input:set, file: str) -> list:
    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        rows = list(reader)
        header = rows[0]

        encoded = []
        # starts at one because header[0] is the movie node
        header_index = 1
        while header_index < len(header):
            if header[header_index] in input:  
                encoded.append(1)
            else:
                encoded.append(0)
            header_index += 1

        return encoded

def get_rec(tree: MovieDecisionTree, input: list) -> list:
    recommendations = tree.traverse_tree(input)
    return recommendations




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
    t = build_decision_tree('decision_tree.csv')

    # root1 = tk.Tk()
    # app = Recommender(root1)
    # root1.mainloop()

    #test getting rec
    # print(t)
    x = convert_user_input({'runtime_bin_mid', 'genre_Comedy', 'genre_Crime', 'genre_Drama'}, 'decision_tree.csv')
    rec = get_rec(t, x)
    y = eval(rec[0])
    print(pickle.loads(y).title)
    # test
    
