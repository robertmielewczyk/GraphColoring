import random
from graphStructure.graph import *
#----------------------------------------------------------------------#
# Legacy Class (useful for checking empty graph) - Delete or change it #
#----------------------------------------------------------------------#
class GraphRandomExample():
    '''
    this class creates random example graph object and sets defined
    random connections and random size

    0--1--3--(...)--itd...      #Random Number of Nodes (within limit)
     \                          #Random Number of connections (Within limit)
      2 (--) (...)
    Note: No colors are assigned to this graph
    '''
    def __init__(self, numberOfNodes=5, numberOfConnections=5, randomConnections=False, randomNodes=False, nodeLimit=10, connectionsLimit=50, hardcodedConnectionsLimit=False):
        if(randomNodes):
            numberOfNodes = random.randint(1,nodeLimit)
        if(not hardcodedConnectionsLimit):
            numberOfConnections = numberOfNodes*numberOfNodes
        self.graph = Graph(numberOfNodes)
        self.__populateGraph(numberOfConnections, randomConnections, connectionsLimit)
    
    def __populateGraph(self, numberOfConnections, randomConnections, connctionsLimit):
        if(randomConnections):
            numberOfConnections = random.randint(1,connctionsLimit)
        for i in range(numberOfConnections):
            node1, node2 = self.__returnRandomConnections(self.graph.numberOfNodes)
            self.graph.addUndirectedConnection(node1, node2)
        
        return self.graph

    def __returnRandomConnections(self, numberOfNodes):
        return random.randint(0, numberOfNodes-1), random.randint(0, numberOfNodes-1)