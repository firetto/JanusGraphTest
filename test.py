from gremlin_python import statics
from gremlin_python.structure.graph import Graph
from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection


# TO RUN IN JUPYTER SERVER, UNCOMMENT THIS CODE:
# !pip install nest_asyncio
# import nest_asyncio
# nest_asyncio.apply()

# REFERENCE: https://www.markhneedham.com/blog/2019/05/10/jupyter-runtimeerror-this-event-loop-is-already-running/




# Instantiate a Gremlin Graph
graph = Graph()

# Connect to the server, instantiate traversal of graph.
g = graph.traversal().withRemote(DriverRemoteConnection('ws://localhost:8182/gremlin','g'))

# Get the vertices of the graph as a list, and print them.
v = g.V().toList()
print(v)