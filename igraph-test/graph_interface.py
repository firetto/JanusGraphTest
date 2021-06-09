"""
graph_interface.py

Contains methods for connecting to Gremlin server and setting up a test graph.

Anatoly Zavyalov, 2021
"""

from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.driver import client
from gremlin_python.process.traversal import P # NEW!!! Import predicates (gt, gte, lt, lte, etc.)
from gremlin_python.process.traversal import Cardinality # NEW!!! Import Cardinality such as list_, set_ and single.
from gremlin_python.driver.protocol import GremlinServerError # Gremlin server error
from gremlin_python.process.traversal import Pop # for Pop.all_ in select(Pop.all_, 'v')
from gremlin_python.process.strategies import SubgraphStrategy

from log_to_file import log_to_file

class GraphInterface:
    """
    A wrapper class for a graph interface, containing methods to intantiate the graph, load a HIRAX-style graph structure, and more.

    :param ALLOWED_VERTEX_LABELS: Contains the allowed labels for vertices in the graph.
    :type ALLOWED_VERTEX_LABELS: tuple
    """

    ALLOWED_VERTEX_LABELS = ('component', 'type')


    def __init__(self, port: int=8182, traversal_source: str='g') -> None:
        """
        Constructor class.

        :param port: The port on which the Gremlin server is located on localhost, defaults to 8182
        :type port: int, optional
        :param traversal_source: The traversal source configured in the Gremlin server for the graph (see https://github.com/JanusGraph/janusgraph/issues/1051 for more), defaults to 'g'
        :type traversal_source: str, optional
        """

        self.graph = Graph()

        try:
            self.g = self.graph.traversal().withRemote(DriverRemoteConnection(f'ws://localhost:{port}/gremlin', traversal_source))
        except GremlinServerError as e:
            log_to_file(message=f"GremlinServerError when trying to instantiate graph traversal. {e}", urgency=2)            


    def add_vertex(self, label: str, name: str, allow_duplicates: bool=False, enforce_label_scheme: bool=True) -> None:
        """
        Add a vertex to the graph with the label :param label: and 'name' property of :param name:.

        :param label: What to label the vertex. 'component' or 'type'.
        :type label: str
        :param name: The 'name' property of the vertex.
        :type name: str
        :param allow_duplicates: Whether to allow vertices of the same label and name to be added, defaults to False
        :type allow_duplicates: bool, optional
        :param enforce_label_scheme: Whether to enforce that the :param label: is in self.ALLOWED_VERTEX_LABELS, defaults to True
        :type enforce_label_scheme: bool, optional
        """

        if not enforce_label_scheme:
            log_to_file(message=f"Adding vertex with label {label}, name {name} without enforcing label naming scheme.", urgency=1)

        elif label not in self.ALLOWED_VERTEX_LABELS:
            log_to_file(message=f"Vertex label {label} is not in {self.ALLOWED_VERTEX_LABELS}", urgency=2)
            # TODO: Make own exception (?), raise it here.
            return

        try:
            if allow_duplicates or self.g.V().has('name', name).count().next() == 0:
                self.g.addV(label).property('name', name).iterate()

            else:
                log_to_file(message=f"Vertex of name {name} already exists.", urgency=2)

        except GremlinServerError as e:
            log_to_file(message=f"Failed to add component of name {name}. {e}", urgency=2)


    def add_component(self, name: str) -> None:
        """
        Add a vertex with label 'component' to the graph with a 'name' property of :param name: if one with this name does not already exist.

        :param name: Value of the 'name' property to assign the vertex to.
        :type name: str
        """

        self.add_vertex(label='component', name=name)


    def add_type(self, type_: str) -> None:
        """
        Add a vertex with label 'type' to the graph with a 'name' property of :param type_:.

        # TODO: figure out better naming for :param type_:.

        :param type_: Value of the 'name' property to assign the vertex to.
        :type type_: str
        """

        self.add_vertex(label='type', name=type_)


    def set_type(self, name: str, type_: str) -> None:
        """
        Connect the component vertex with name property :param name: to a type vertex labelled :param type_: with an edge going into the :param type_: vertex labelled with "type".

        # TODO: figure out better naming for :param type_:.

        :param name: Value of the 'name' property of the component vertex to connect to the type vertex.
        :type name: str
        :param type_: Value of the 'name' property of the type vertex.
        :type type_: str
        """

        try:
            self.g.V().has('component', 'name', name).as_("a").V().has('type', 'name', type_).as_("b").addE("type").from_("a").to("b").iterate()

        except GremlinServerError as e:
            log_to_file(message=f"Failed to set type of component {name} to type {type_}. {e}", urgency=2)


    def set_connection(self, name1: str, name2: str, time: float, connection: bool) -> None:
        """
        Given two vertices labelled with :param name1: and :param name2:, create a new connection or terminate their existing connection, 
        based on the value of :param connection:. Label with time :param time:.

        :param name1: Value of the 'name' property of the first vertex.
        :type name1: str
        :param name2: Value of the 'name' property of the second vertex.
        :type name2: str
        :param time: Time at which the connection was altered.
        :type time: float
        :param connection: True if a connection was created, False otherwise.
        :type connection: bool
        """

        try:
            if connection:
                # Add an edge labelled 'connection' with a start time of :param time:
                self.g.V().has('component', 'name', name1).as_("a").not_( # NEGATE 
                    __.bothE('connection').as_('e').bothV().has('component', 'name', name2).select('e').and_(
                        __.has('start', P.lte(time)),
                        __.or_(
                            __.hasNot('end'),
                            __.has('end', P.gt(time))
                        )
                    )
                ).V().has('component', 'name', name2).as_("b").addE('connection').from_("a").to("b").property('start', time).iterate()

            else:
                # For all edges between v1 and v2 labelled 'connection' (there should only be one) that do not have an 'end' property, create an end property of :param time:.
                self.g.V().has('component', 'name', name1).bothE('connection').as_('e').bothV().has('component', 'name', name2).select('e').hasNot('end').property('end', time).iterate()

        except GremlinServerError as e:
            log_to_file(message=f"Failed to set {connection} connection between components {name1} and {name2} at time {time}. {e}", urgency=2)
