"""Module Description
==================
This module implements a Tkinter-based graphical user interface (Welcome Screen, preference selection,
results display) for PickMeWatchMe.

It contains a Recommender class and get_rec and build_decision_tree functions.

For Genre and Runtime-Based search:
- Builds a binary decision tree from a CSV dataset
- Traverses the tree for relevant movie suggestions based on user input

For Actor-Based Search:
- Loads a movie-actor graph from the dataset.
- Retrieves movie recommendations based on a user-inputted actor.

Copyright and Usage Information
===============================

This file is solely for the personal and private use of
Victoria Cai, Isabella Zhong, Maya Dowman, Grace-Keyi Wang. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2025 Victoria Cai, Isabella Zhong, Maya Dowman, Grace-Keyi Wang
"""

from typing import Any
import csv
import pickle
import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from tree import MovieDecisionTree, BinaryCSV, Movie
from movie_actor_graph import Graph, load_movie_actor_graph


def get_rec(tree: MovieDecisionTree, _input: list) -> list:
    """
    return the recommended films by traversing the given tree
    """
    recommendations = tree.traverse_tree(_input)
    return recommendations


def build_decision_tree(file: str) -> MovieDecisionTree:
    """
    build the decision tree using the given file and returns a MovieDecisionTree object
    """
    tree = MovieDecisionTree('', [])
    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            movie = pickle.loads(eval(row[0]))
            movie_list = row[1:] + [movie]
            tree.create_branch(movie_list)
    return tree


class Recommender:
    """
    Class for the full graphic user interface for PickMeWacthMe.
    """

    root: Any
    title_font: tkfont.Font
    button_font: tkfont.Font
    welcome_frame: tk.Frame
    actor_frame: tk.Frame
    recommendation_frame: tk.Frame
    graph: Graph
    colour_blue: str
    colour_dark: str
    colour_light: str
    actor_entry: tk.Entry
    length_var: tk.StringVar
    genre_listbox: tk.Listbox

    def __init__(self, root: Any) -> None:
        # Initialize the main window and main variables
        self.root = root
        self.root.title("PickMeWatchMe")
        self.root.geometry("800x600")
        self.root.configure(bg="#002138")

        # Initialize recommendation functionality components
        # self.tree = Binary_Csv('imdb_top_1000.csv', 'decision_tree.csv').create_decision_csv()
        self.graph = load_movie_actor_graph("imdb_top_1000.csv")

        # Custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = tkfont.Font(family="Helvetica", size=12)

        # Create frames
        self.welcome_frame = tk.Frame(root, bg="#002138")
        self.actor_frame = tk.Frame(root, bg="#002138")
        self.recommendation_frame = tk.Frame(root, bg="#002138")

        # Colour codes
        self.colour_dark = "#0F6BAE"
        self.colour_blue = "#83B8FF"
        self.colour_light = "#C6CDFF"

        # Initialize UI
        self.create_welcome_screen()

        # Initialize user input as None
        self.actor_entry = None
        self.length_var = None
        self.genre_listbox = None

    def extract_title(self, movie: Movie) -> str:
        """Extract and return the title from the given movie.
        """
        return movie.title

    def convert_user_input(self, _input: set, file: str) -> list:
        """
        Encode the user input into a binary list so that it can traversre through the list.
        """
        with open(file) as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)
            header = rows[0]

            encoded = []
            # starts at one because header[0] is the movie node
            header_index = 1
            while header_index < len(header):
                if header[header_index] in _input:
                    encoded.append(1)
                else:
                    encoded.append(0)
                header_index += 1

            return encoded

    def create_welcome_screen(self) -> None:
        """
        Create the welcome screen for PickMeWatchMe.
        """
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.welcome_frame, text="Welcome to", font=self.title_font,
                 fg="#83B8FF", bg="#002138").pack(pady=20)
        tk.Label(self.welcome_frame, text="PickMeWatchMe!", font=self.title_font,
                 fg="#C6CDFF", bg="#002138").pack(pady=10)

        #  Start button. If clicked go to actor screen
        start_btn = tk.Button(self.welcome_frame, text="Start Matching",
                              command=self.show_actor_screen,
                              font=self.button_font, fg="purple", bg="#0F6BAE",
                              activebackground="#3E8E41", activeforeground="white",
                              borderwidth=0, highlightthickness=0)
        start_btn.pack(pady=40, ipadx=20, ipady=10)

    def show_actor_screen(self) -> None:
        """
        Display the screen asking if the user has an actor/actress in mind.
        """
        # Hide other frames
        self.welcome_frame.pack_forget()
        self.recommendation_frame.pack_forget()

        # Show actor frame
        self.actor_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)

        tk.Label(self.actor_frame, text="If you would like an Actor/Actress-only based search,\nEnter the actor/actress"
                                        "you would like to watch:",
                 font=("Helvetica", 16), fg="white", bg="#002138").pack(pady=20)

        self.actor_entry = tk.Entry(self.actor_frame, width=30, font=self.button_font,
                                    bg=self.colour_light, fg=self.colour_dark, highlightthickness=0,
                                    borderwidth=0, insertbackground="white")
        self.actor_entry.pack(pady=10, ipady=5)

        btn_frame = tk.Frame(self.actor_frame, bg="#002138")
        btn_frame.pack(pady=20)

        # Enter the inputted actor, goes to the graph functionality
        enter_btn = tk.Button(btn_frame, text="Enter Actor (Case Sensitive)",
                              command=self.handle_actor_search,
                              font=self.button_font, fg="purple", bg=self.colour_blue,
                              activebackground="#3E8E41", activeforeground="white",
                              borderwidth=0, highlightthickness=0)
        enter_btn.pack(side=tk.LEFT, padx=10)

        # Skip to rest of recommendation system by calling tree functionality
        skip_btn = tk.Button(btn_frame, text="Skip to Runtime/Genre Search",
                             command=self.show_tree_recommendations,
                             font=self.button_font, fg="purple", bg=self.colour_blue,
                             activebackground="#FF3737", activeforeground="white",
                             borderwidth=0, highlightthickness=0)
        skip_btn.pack(side=tk.LEFT, padx=10)

    def handle_actor_search(self) -> None:
        """
        Recommend movies based on the actor the user inputted.
        """
        actor_name = self.actor_entry.get()  # gets the inputted actor's name
        if actor_name:
            if actor_name not in self.graph.get_vertices('actor'):
                messagebox.showinfo("Sorry", f"{actor_name} is not in our Database")
                return

            movies = self.graph.get_neighbours(actor_name)
            if movies:
                self.show_movie_list(movies, f"Movies featuring {actor_name}")
            else:
                messagebox.showinfo("Not Found", f"No movies found for {actor_name}")

        else:  # no actor name inputted
            messagebox.showwarning("Input Error", "Please enter an actor's name")

    def show_tree_recommendations(self) -> None:
        """
        Show recommendations by using the tree.
        """
        self.actor_frame.pack_forget()
        self.welcome_frame.pack_forget()

        self.recommendation_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)

        tk.Label(self.recommendation_frame,
                 text="Please select your preferences:",
                 font=("Helvetica", 16), fg="white", bg="#002138").pack(pady=20)

        # Runtime dropdown
        length_frame = tk.Frame(self.recommendation_frame, bg="#002138")
        length_frame.pack(pady=10)

        tk.Label(length_frame, text="Runtime:",
                 font=self.button_font, fg="white", bg="#002138").pack(side=tk.LEFT, padx=10)

        length_options = ["0-60 minutes", "60-90 minutes", "90-120 minutes",
                          "120-180 minutes", "180-240 minutes", "240+ minutes"]
        self.length_var = tk.StringVar(value=length_options[0])
        length_dropdown = tk.OptionMenu(length_frame, self.length_var, *length_options)
        length_dropdown.config(font=self.button_font, bg=self.colour_blue, fg="white",
                               activebackground=self.colour_dark, activeforeground="white",
                               highlightthickness=0)
        length_dropdown["menu"].config(font=self.button_font, bg=self.colour_light, fg=self.colour_dark)
        length_dropdown.pack(side=tk.LEFT)

        # Genre multiple-selection Listbox
        genre_frame = tk.Frame(self.recommendation_frame, bg="#002138")
        genre_frame.pack(pady=10)

        tk.Label(genre_frame, text="Select Genre(s):",
                 font=self.button_font, fg="white", bg="#002138").pack(side=tk.LEFT, padx=10)

        genre_options = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime",
                         "Drama", "Family", "Fantasy", "Film-Noir", "History", "Horror",
                         "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Support",
                         "Thriller", "War", "Western"]

        # self.genre_var = tk.StringVar(value=genre_options[0])
        # genre_dropdown = tk.OptionMenu(genre_frame, self.genre_var, *genre_options)
        # genre_dropdown.config(font=self.button_font, bg=self.colour_blue, fg="white",
        #                        activebackground=self.colour_dark, activeforeground="white",
        #                        highlightthickness=0)
        # genre_dropdown["menu"].config(font=self.button_font, bg=self.colour_light, fg=self.colour_dark)
        # genre_dropdown.pack(side=tk.LEFT)
        #  listbox to allow multiple selections
        self.genre_listbox = tk.Listbox(genre_frame, selectmode="multiple",
                                        font=self.button_font, bg=self.colour_light,
                                        fg=self.colour_dark, height=10)

        for genre in genre_options:
            self.genre_listbox.insert(tk.END, genre)

        scrollbar = tk.Scrollbar(genre_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.genre_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.genre_listbox.yview)

        self.genre_listbox.pack(side=tk.LEFT)

        # Submit button
        submit_btn = tk.Button(self.recommendation_frame, text="Submit",
                               command=self.process_preferences,  # call processing function
                               font=self.button_font, fg="purple", bg=self.colour_blue,
                               activebackground="#3E8E41", activeforeground="white",
                               borderwidth=0, highlightthickness=0)
        submit_btn.pack(pady=20)

    def process_preferences(self) -> None:
        """
        Store the preferences into a tuple
        """
        length_map = {
            "0-60 minutes": "runtime_bin_very-short",
            "60-90 minutes": "runtime_bin_short",
            "90-120 minutes": "runtime_bin_mid",
            "120-180 minutes": "runtime_bin_mid-long",
            "180-240 minutes": "runtime_bin_long",
            "240+ minutes": "runtime_bin_very-long"
        }
        genre_map = {
            "Action": "genre_Action",
            "Animation": "genre_Animation",
            "Adventure": "genre_Adventure",
            "Biography": "genre_Biography",
            "Comedy": "genre_Comedy",
            "Crime": "genre_Crime",
            "Drama": "genre_Drama",
            "Family": "genre_Family",
            "Fantasy": "genre_Fantasy",
            "Film-Noir": "genre_Film-Noir",
            "History": "genre_History",
            "Horror": "genre_Horror",
            "Music": "genre_Music",
            "Musical": "genre_Musical",
            "Mystery": "genre_Mystery",
            "Romance": "genre_Romance",
            "Sci-Fi": "genre_Sci-Fi",
            "Support": "genre_Support",
            "Thriller": "genre_Thriller",
            "War": "genre_War",
            "Western": "genre_Western"
        }

        length = {length_map[self.length_var.get()]}
        selected_indices = self.genre_listbox.curselection()
        genres = {genre_map[self.genre_listbox.get(i)] for i in selected_indices}
        encoded_input = length.union(genres)

        # call the encoding and tree traversal functions
        BinaryCSV('imdb_top_1000.csv', 'decision_tree.csv').create_decision_csv()
        decision_tree = build_decision_tree('decision_tree.csv')  # create decision tree
        encoded = self.convert_user_input(encoded_input, 'decision_tree.csv')
        recommended_movies = get_rec(decision_tree, encoded)  # get movie recommendations
        if recommended_movies == 'Not Found':
            messagebox.showinfo("No Recommendations", "No movie recommendations found for your preferences.")
        elif recommended_movies:
            self.show_movie_list(recommended_movies, "Movie Recommendations")

    def show_movie_list(self, movies: list, title: str) -> None:
        """
        Show the list of movie recommendations in a window.
        Display only movie titles since the vertices are just movie titles.
        """
        # Create result window
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("400x600")

        style = ttk.Style(result_window)
        style.configure("Treeview", font=("Helvetica", 12), rowheight=25)
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))

        # Tree showcase of movie recommendations
        tree = ttk.Treeview(result_window, columns=("Title",), show="headings")

        # Define column heading
        tree.heading("Title", text="Movie Title")

        # Adjust column width
        tree.column("Title", width=350, anchor="center")

        # Insert data into the tree
        for movie in movies:
            if isinstance(movie, Movie):  # Check if it's a Movie object
                movie_title = self.extract_title(movie)
                tree.insert("", tk.END, values=(movie_title,))
            else:
                tree.insert("", tk.END, values=(movie,))  # Movie is a string (title)

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")


if __name__ == '__main__':

    import python_ta.contracts
    import doctest

    python_ta.contracts.check_all_contracts()

    doctest.testmod(verbose='TRUE')

    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'tkinter.font', 'tree', '__future__',
                          'movie_actor_graph', 'tree', 'csv', 'pickle', 'tree', 'ast'],
        'allowed-io': ['build_decision_tree', 'load_movie_data', 'encode_user_input', 'convert_user_input'],
        'max-line-length': 120
    })
