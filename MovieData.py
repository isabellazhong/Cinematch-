import csv
import dataclasses

class MovieData:
    """Data object representing movie data

    Instance Attributes:
        - genre: The genre of this film
        - runtime: the runtime of this film
        - cast: a list of main actors in this film
        - director: the director of this film
    """
    title: str
    genre: str
    runtime: int
    cast: list[str]
    director: list[str]
    movie_id = str

    def __init__(self, title, genre, runtime, cast, director, movie_id):
        self.title = title
        self.genre = genre
        self.runtime = runtime
        self.cast = cast
        self.director = director
        self.movie_id = movie_id

    @classmethod
    def load_movie_basics(cls) -> dict:
        """
        class method to load in the basic information of the movie. Returns a dictionary mapping the unique movie id
        identifier to the MovieData object of the specific movie.
        """
        movies = {}
        with open("data/title.basics.tsv") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                movie_id = row["tconst"]
                title = row["primaryTitle"]
                genre = row["genres"]
                runtime = row["runtimeMinutes"]
                movies[movie_id] = cls(title, genre, runtime, [], [], movie_id)
        return movies

    @classmethod
    def load_directors_cast(cls, movies: dict[str: "MovieData"]) -> None:
        """
        class method to load in the directors and cast information of the movie. Mutates the dictionary mapping the
        unqique movie id identifier to the MovieData object.
        """
        with open("data/title.principals.tsv") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                if row["ttconst"] in movies:
                    if row["category"] == "director":
                        movies["ttconst"].director.append(row["director"])
                    if row["category"] == "actor" or row["category"] == "actress":
                        movies["ttconst"].actors.append(row["category"])
            return
    @classmethod
    def load_full_data(cls):
        """
        class method to create the full MovieData object for all movies
        """
        movies = cls.load_movie_basics()
        cls.load_directors_cast(movies)
        return movies
