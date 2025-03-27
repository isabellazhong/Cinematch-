import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
from tree import Movie
from MovieActorGraph import _Vertex, Graph, load_movie_actor_graph
from MovieData import MovieData


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
        self.tree = Movie()
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
                              font=self.button_font, fg="white", bg="#0F6BAE",
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
                               font=self.button_font, fg="white", bg=self.colour_blue,
                               activebackground="#3E8E41", activeforeground="white",
                               borderwidth=0, highlightthickness=0)
        enter_btn.pack(side=tk.LEFT, padx=10)

        # Skip to rest of recommendation system by calling tree functionality
        skip_btn = tk.Button(btn_frame, text="Skip to Recommendations",
                             command=self.show_tree_recommendations,
                             font=self.button_font, fg="white", bg=self.colour_blue,
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

        # TODO: Add screen for asking questions: "What is the runtime range you're looking to be within?"
        # "What genre movie would you like to watch?" use tree to filter through.

    def show_movie_list(self, movies, title):
        """
        Shows the list of movie recommendations in a window
        """
        # Create result window
        result_window = tk.Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("600x400")

        style = ttk.Style(result_window)
        style.configure("Treeview", font=("Arial", 12), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))

        # Tree showcase of movie recommendations
        tree = ttk.Treeview(result_window, columns=("Title", "Year", "Rating"), show="headings")
        tree.heading("Title", text="Movie Title")
        tree.heading("Year", text="Year")
        tree.heading("Rating", text="Rating")

        for movie in movies:
            if isinstance(movie, dict):
                tree.insert("", tk.END, values=(movie.get('title', ''), 
                                                movie.get('year', ''), 
                                                movie.get('rating', '')))
            elif isinstance(movie, str):
                tree.insert("", tk.END, values=(movie, '', ''))
            else:
                tree.insert("", tk.END, values=(getattr(movie, 'title', ''),
                                                getattr(movie, 'year', ''),
                                                getattr(movie, 'rating', '')))

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
