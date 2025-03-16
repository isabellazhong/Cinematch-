from __future__ import annotations
import csv
from typing import Any


class _Vertex:
    """A vertex in an Actor-Movie graph, used to represent an actor or a movie.

    Each vertex item is either an FULL NAME or a movie title, represented as strings.

    Instance Attributes:
        - item: The data stored in this vertex, representing an actor or a movie.
        - kind: The type of this vertex: 'actor' or 'movie'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'actor', 'movie'}
    """
    item: Any
    kind: str
    neighbours: set[_Vertex]

    def __init__(self, item: str, kind: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - kind in {'movie', 'actor'}
        """
        self.item = item
        self.kind = kind
        self.neighbours = set()


class Graph:
    """A graph used to represent actors and the movies they've been in.
    """
    # Private Instance Attributes:
    #     - _vertices:
    #         A collection of the vertices contained in this graph.
    #         Maps item to _Vertex object.
    _vertices: dict[Any, _Vertex]

    def __init__(self) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}

    def add_vertex(self, item: str, kind: str) -> None:
        """Add a vertex with the given item and kind to this graph.

        The new vertex is not adjacent to any other vertices.
        Do nothing if the given item is already in this graph.

        Preconditions:
            - kind in {'actor', 'movie'}
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def add_edge(self, item1: str, item2: str) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """

        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def get_neighbours(self, item: str) -> set:
        """Return a set of the neighbours of the given item.

        Note that the *items* are returned, not the _Vertex objects themselves.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item in self._vertices:
            v = self._vertices[item]
            return {neighbour.item for neighbour in v.neighbours}
        else:
            raise ValueError


def load_movie_actor_graph(movie_file: str) -> Graph:
    """Return a graph corresponding to the given datasets.

    The book review graph stores all the information from the movie_file as follows:
    Create one vertex for each actor and one vertex for each movie.
    Edges represent an actor being in a movie.

    The vertices of the 'actor' kind should have the 'actor's FULL NAME' as its item.
    The vertices of the 'movie' kind representing each reviewed book should have the movie TITLE as its item.

    Preconditions:
        - movie_file is the path to a CSV file corresponding to the movie data
    """

    graph = Graph()

    with open(movie_file) as f:
        reader = csv.reader(f, delimiter="\t", quotechar='"')
        for row in reader:

            print(row)

    # FINISH WHEN I CAN SEE THE TSV FILE

    return graph


if __name__ == '__main__':
    # You can uncomment the following lines for code checking/debugging purposes.
    # However, we recommend commenting out these lines when working with the large
    # datasets, as checking representation invariants and preconditions greatly
    # increases the running time of the functions/methods.
    # import python_ta.contracts
    # python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136'],
        'extra-imports': ['csv', 'networkx'],
        'allowed-io': ['load_review_graph'],
        'max-nested-blocks': 4
    })
