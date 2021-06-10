"""
local_graph.py

Contains the LocalGraph class, which contains an igraph.Graph instance and some methods to access and modify it.
Used for subgraphs in a GraphInterface.

Anatoly Zavyalov, 2021
"""

import igraph

class LocalGraph():
    """

    A wrapper class for an igraph.Graph instance.

    :ivar graph: Contains the igraph Graph.
    """

    graph: igraph.Graph


    def __init__(self) -> None:
        """
        Instantiate an empty igraph.Graph instance.        
        """

        self.graph = igraph.Graph()


    def create_from_connections_undirected(self, vertex_connections: list[tuple[str, str]]) -> None:
        """
        Instantiate a simple undirected igraph.Graph given pairs of vertices to connect.

        :param vertex_connections: A list of the format [(name1, name2), (name3, name4), ...] where name# represents the names of the vertices.
        :type vertex_connections: list[tuple[str, str]]
        """

        # See https://igraph.org/python/doc/api/igraph.formula.html for help regarding igraph Formulas.

        # Start a formula
        formula = ", ".join([f"'{name1}'--'{name2}'" for (name1, name2) in vertex_connections])

        self.graph = igraph.Graph.Formula(formula)
        

    def visualize_graph(self, target: str) -> None:
        """Export the graph as an image to :param target:.

        :param target: File location to export the file to. Should be in PNG, PDF, SVG or PostScript format.
        :type target: str
        """

        igraph.plot(self.graph, target=target)
    