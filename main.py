import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from MovieActorGraph import _Vertex, Graph, load_movie_actor_graph
from MovieData import MovieData
import csv
from tree import Movie, MovieDecisionTree


class CineMatch:
    """
    Class for the full graphic user interface for CineMatch.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("CineMatch")
        self.root.geometry("800x600")
        self.root.configure(bg="#002138")

        # Initialize recommendation functionality components
        # self.tree = Movie()
        self.graph = load_movie_actor_graph("imdb_top_1000.csv")

        # Custom fonts
        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = tkfont.Font(family="Helvetica", size=12)

        # Create frames
        self.welcome_frame = tk.Frame(root, bg="#002138")
        self.actor_frame = tk.Frame(root, bg="#002138")
        self.recommendation_frame = tk.Frame(root, bg="#002138")

        # Initialize UI
        self.create_welcome_screen()

        # Colour codes
        self.colour_dark = "#0F6BAE"
        self.colour_blue = "#83B8FF"
        self.colour_light = "#C6CDFF"

    def create_welcome_screen(self):
        """
        Creates the welcome screen for CineMatch.
        :return:
        """
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(self.welcome_frame, text="Welcome to", font=self.title_font,
                 fg="#83B8FF", bg="#002138").pack(pady=20)
        tk.Label(self.welcome_frame, text="CineMatch!", font=self.title_font,
                 fg="#C6CDFF", bg="#002138").pack(pady=10)

        #  Start button. If clicked go to actor screen
        start_btn = tk.Button(self.welcome_frame, text="Start Matching",
                              command=self.show_actor_screen,
                              font=self.button_font, fg="purple", bg="#0F6BAE",
                              activebackground="#3E8E41", activeforeground="white",
                              borderwidth=0, highlightthickness=0)
        start_btn.pack(pady=40, ipadx=20, ipady=10)

    def show_actor_screen(self):
        """
        Display the screen asking if the user has an actor/actress in mind.
        """
        self.welcome_frame.pack_forget()
        self.actor_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)

        tk.Label(self.actor_frame, text="(Optional) Enter the actor/actress you would like to watch:",
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
        skip_btn = tk.Button(btn_frame, text="Skip to Recommendations",
                             command=self.show_tree_recommendations,
                             font=self.button_font, fg="purple", bg=self.colour_blue,
                             activebackground="#FF3737", activeforeground="white",
                             borderwidth=0, highlightthickness=0)
        skip_btn.pack(side=tk.LEFT, padx=10)

    def handle_actor_search(self):
        """
        Recommend movies based on the actor the user inputted.
        """
        actor_name = self.actor_entry.get()  # gets the inputted actor's name
        if actor_name:
            movies = self.graph.get_neighbours(actor_name)
            if movies:
                self.show_movie_list(movies, f"Movies featuring {actor_name}")
            else:
                messagebox.showinfo("Not Found", f"No movies found for {actor_name}")

        else:  # no actor name inputted
           messagebox.showwarning("Input Error", "Please enter an actor's name")

    def show_tree_recommendations(self):
        """
        Shows recommendations by using the tree.
        """
        self.actor_frame.pack_forget()
        self.recommendation_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)

        tk.Label(self.recommendation_frame,
                 text="Please select your preferences:",
                 font=("Helvetica", 16), fg="white", bg="#002138").pack(pady=20)

        # Runtime dropdown
        length_frame = tk.Frame(self.recommendation_frame, bg="#002138")
        length_frame.pack(pady=10)

        tk.Label(length_frame, text="Runtime:",
                 font=self.button_font, fg="white", bg="#002138").pack(side=tk.LEFT, padx=10)

        length_options = ["0-60 minutes", "60-90 minutes", "90-120 minutes", "120-180 minutes", "180-240 minutes", "240+ minutes"]
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
                               command= self.process_preferences,  # call processing function
                               font=self.button_font, fg="purple", bg=self.colour_blue,
                               activebackground="#3E8E41", activeforeground="white",
                               borderwidth=0, highlightthickness=0)
        submit_btn.pack(pady=20)

    def process_preferences(self):
        """
        Stores the preferences into a tuple
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

        length = length_map[self.length_var.get()]
        # Get selected genres from Listbox
        selected_indices = self.genre_listbox.curselection()
        genres = {genre_map[self.genre_listbox.get(i)] for i in selected_indices}

        length = length_map[self.length_var.get()]

        selected_indices = self.genre_listbox.curselection()
        genres = {genre_map[self.genre_listbox.get(i)] for i in selected_indices}

        encoded_input = (length, tuple(genres))

        convert_user_input(encoded_input, 'decision_tree.csv')

        recommended_movies = get_rec()
        if recommended_movies:
            self.show_movie_list(recommended_movies, "Movie Recommendations")
        else:
            messagebox.showinfo("No Recommendations", "No movie recommendations found for your preferences.")



    def show_movie_list(self, movies, title):
            """
            Shows the list of movie recommendations in a window
            """
            # Create result window
            result_window = tk.Toplevel(self.root)
            result_window.title(title)
            result_window.geometry("800x600")  # Increased width for better layout

            style = ttk.Style(result_window)
            style.configure("Treeview", font=("Helvetica", 12), rowheight=25)
            style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"))

            # Tree showcase of movie recommendations
            tree = ttk.Treeview(result_window,
                                columns=("Title", "Year", "Genre", "Runtime", "Rating", "Director", "Cast"),
                                show="headings")

            # Define column headings
            tree.heading("Title", text="Movie Title")
            tree.heading("Year", text="Year")
            tree.heading("Genre", text="Genre")
            tree.heading("Runtime", text="Runtime")
            tree.heading("Rating", text="Rating")
            tree.heading("Director", text="Director")

            # Adjust column widths if needed
            tree.column("Title", width=150)
            tree.column("Genre", width=120)
            tree.column("Runtime", width=60)
            tree.column("Rating", width=50)
            tree.column("Director", width=120)

            # Insert data into the tree
            for movie in movies:
                if isinstance(movie, MovieData):  # movie should be a MovieData instance
                    tree.insert("", tk.END, values=(
                        movie.poster_title[1],          # Movie Title
                        movie.genre_runtime[0],         # Genre
                        movie.genre_runtime[1],         # Runtime
                        movie.overview_rating[1],       # Rating
                        movie.cast_director[1],        # Director
                    ))
            tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")


# Configure styles
style = ttk.Style()
style.theme_use('clam')
style.configure('Dark.TFrame', background='#2A2A2A')
style.configure('Accent.TButton', font=('Arial', 14),
                foreground='white', background='#4ECDC4')
style.configure('Secondary.TButton', font=('Arial', 14),
                foreground='white', background='#FF6B6B')

def build_decision_tree(file:str) -> None:
    tree = MovieDecisionTree(None, [])
    with open(file) as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            movie = row[0]
            movie_list = row[1:] + [movie]
            tree.create_branch(movie_list)

#encodes the user input into a binary list so that it can traversre through the list
def convert_user_input(input:tuple, file: str) -> list:
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

#TODO add this method
def get_rec(tree: MovieData, input:list) -> None:
    return

if __name__ == "__main__":
# You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    # import doctest
    #
    # doctest.testmod()
    #
    # import python_ta
    #
    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['E1136'],
    #     'extra-imports': ['csv', 'networkx'],
    #     'allowed-io': ['load_movie_actor_graph'],
    #     'max-nested-blocks': 4
    # })
    root1 = tk.Tk()
    app = CineMatch(root1)
    root1.mainloop()
    # test
    print(convert_user_input(('runtime_bin_short', 'genre_Family'), 'decision_tree.csv'))
