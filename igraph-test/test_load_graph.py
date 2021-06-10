"""
test_load_graph.py

Contains methods for loading a HIRAX-style graph, timing, then setting up connections.


(Temporary) Naming scheme:
 - COR######: Correlator input
 - ANT######: Antenna
 - DPF######: Dual-Polarization Feed
 - BLN######: (Active) Balun
 - RFT######: RFoF transmitter
 - OPF######: Optical Fiber
 - RFR######: RFoF receiver
 - ADC######: Analog-to-Digital converter


Anatoly Zavyalov, 2021
"""

from graph_interface import GraphInterface
from gremlin_python.driver.protocol import GremlinServerError # Gremlin server error

from log_to_file import log_to_file

from datetime import datetime


def clear_graph(gi: GraphInterface) -> None:
    """

    Clear the graph stored in the graph traversal of the GraphInterface.

    # TODO: THIS FUNCTION IS FOR TESTING PURPOSES ONLY. 

    :param gi: The GraphInterface containing a graph.
    :type gi: GraphInterface
    """

    log_to_file(message=f"Dropping graph!", urgency=1)

    success = False
    while not success:
        
        try:
            gi.g.V().drop().iterate()
            success = True

        except GremlinServerError as e:
            log_to_file(message=f"Error while trying to drop all vertices. {e}", urgency=1)

    

def load_graph(dishes: int, connections: list) -> GraphInterface:
    """

    Instantiate a GraphInterface, and set up a HIRAX-style graph with :param dishes: dishes with each pair of components in the 
    signal chain being connected and disconnected identically based on :param connections:.

    :param dishes: Number of dishes the graph will contain.
    :type dishes: int
    :param connections: A list of (float, bool) 2-tuples, where the first element is the time and the second element is whether a connection was started or stopped at that time. List must be sorted by time, and each second element must alternate.
    :type connections: list
    :return: A GraphInterface instance containing the graph traversal to the instantiated graph.
    :rtype: GraphInterface
    """

    gi = GraphInterface()

    # Clear entire graph.
    clear_graph(gi)

    # Correlator node name
    cor = 'COR000000'

    # Set up the types
    types = ['COR', 'ANT', 'DPF', 'BLN', 'RFT', 'OPF', 'RFR', 'ADC']

    total = 0

    now = datetime.now()

    for t in types:
        gi.add_type(t)

    # Add a correlator input node
    gi.add_component(cor)
    gi.set_type(cor, 'COR')

    total += (datetime.now() - now).total_seconds()

    # Add the components and connect them at different times.
    for i in range(1, dishes + 1):

        # The names of the components to refer to
        ant = f'ANT{str(i).zfill(6)}'
        dpf = f'DPF{str(i).zfill(6)}'
        bln = (f'BLN{str(2 * i - 1).zfill(6)}', f'BLN{str(2 * i).zfill(6)}')
        rft = (f'RFT{str(2 * i - 1).zfill(6)}', f'RFT{str(2 * i).zfill(6)}')
        opf = (f'OPF{str(2 * i - 1).zfill(6)}', f'OPF{str(2 * i).zfill(6)}')
        rfr = (f'RFR{str(2 * i - 1).zfill(6)}', f'RFR{str(2 * i).zfill(6)}')
        adc = (f'ADC{str(2 * i - 1).zfill(6)}', f'ADC{str(2 * i).zfill(6)}')

        now = datetime.now()

        gi.add_component(ant)
        gi.add_component(dpf)

        gi.set_type(ant, 'ANT')
        gi.set_type(dpf, 'DPF')

        for ind in (0, 1):
            gi.add_component(bln[ind])
            gi.add_component(rft[ind])
            gi.add_component(opf[ind])
            gi.add_component(rfr[ind])
            gi.add_component(adc[ind])

            gi.set_type(bln[ind], 'BLN')
            gi.set_type(rft[ind], 'RFT')
            gi.set_type(opf[ind], 'OPF')
            gi.set_type(rfr[ind], 'RFR')
            gi.set_type(adc[ind], 'ADC')

        for (time, connection) in connections:

            gi.set_connection(name1=ant, name2=dpf, time=time, connection=connection)

            for ind in (0, 1):

                # Pairs of names to connect
                pairs = [(ant, dpf), (dpf, bln[ind]), (bln[ind], rft[ind]), (rft[ind], opf[ind]), (opf[ind], rfr[ind]), (rfr[ind], adc[ind]), (adc[ind], cor)]

                for pair in pairs:
                    gi.set_connection(name1=pair[0], name2=pair[1], time=time, connection=connection)

        delta = (datetime.now() - now).total_seconds()

        total += delta

        log_to_file(message=f"Adding dish {i} done, took {delta} seconds.")
    
    log_to_file(message=f"Graph with {dishes} dishes loaded, took {total} total seconds.")

    return gi

if __name__ == "__main__":
    gi = load_graph(dishes=4, connections=[(1, True)])

    gi.export_graph('test_load_graph.xml')
        

