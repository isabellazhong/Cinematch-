"""A class for movie data."""
import csv


class MovieData:
    """Data object representing movie data

    Instance Attributes:
        - poster_title: a tuple contaning an address for the movie poster image and the movie title
        - genre_runtime: a tuple containing the movie genre and runtime
        - cast_director: a tuple containing a list of the movie cast members and the movie director
        - overview_rating: a tuple containing the movie overview and the movie rating
    """

    poster_title: tuple[str, str]
    genre_runtime: tuple[str, int]
    cast_director: tuple[list[str], str]
    overview_rating: tuple[str, float]

    def __init__(self, poster_title, genre_runtime, cast_director, overview_rating):
        self.poster_title = poster_title
        self.genre_runtime = genre_runtime
        self.cast_director = cast_director
        self.overview_rating = overview_rating

    def __str__(self) -> str:
        """Return a string representation of the MovieData object."""
        return (f"Title: {self.poster_title[1]}\n"
                f"Genre: {self.genre_runtime[0]}\n"
                f"Runtime: {self.genre_runtime[1]}\n"
                f"Director: {self.cast_director[1]}\n"
                f"Cast: {', '.join(self.cast_director[0])}\n"
                f"IMDB Rating: {self.overview_rating[1]}\n"
                f"Overview: {self.overview_rating[0]}")

    @classmethod
    def load_movie_basics(cls, filename: str) -> dict:
        """
        class method to load in the basic information of the movie. Returns a dictionary mapping the unique movie id
        identifier to the MovieData object of the specific movie.
        """
        movies = {}
        with open(filename) as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                poster_title = (row["Poster_Link"], row["Series_Title"])
                genre_runtime = (row["Genre"], row["Runtime"])
                cast_director = ([row["Star1"], row["Star2"], row["Star3"], row["Star4"]], row["Director"])
                overview_rating = (row["Overview"], row["IMDB_Rating"])
                movies[row["Series_Title"]] = MovieData(poster_title, genre_runtime, cast_director, overview_rating)
        return movies
    

  


