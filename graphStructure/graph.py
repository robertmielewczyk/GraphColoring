import random
class Node:
    def __init__(self):
        self.__color = 0
        self.__connections = []

    def setConnections(self, connections):
        self.__connections = connections

    def getConnections(self):
        return self.__connections
    
    def getColor(self):
        return self.__color

    def setColor(self, color):
        self.__color = color
    
    def addConnection(self, otherNode):
        self.__connections.append(otherNode)

    def ToString(self):
        return "Color: "+str(self.__color)+" Connections: "+str(self.__connections)

class Graph:
    #-------------------------------------------------------------#
    # Constructor - graph loads from file if not then empty graph #
    #-------------------------------------------------------------#
    def __init__(self, file=False):
        if(file):
            self.__loadGraph(file)
        else:
            self.numberOfNodes = 0
            self.nodes = {}

    #----------------------#
    # Saving Loading Graph #
    #----------------------#
    def __loadGraph(self, filePath):
        import yaml
        with open(filePath, 'r') as file:
            #Load Graph file
            graph = yaml.load(file, Loader=yaml.FullLoader)

            #Initialize numberOfNode and nodes dictionary
            self.numberOfNodes = graph['nodes']
            self.nodes = {}
            for node in range(graph['nodes']):
                self.nodes[node] = Node()
                self.nodes[node].setConnections(graph['connections'][node])
                self.nodes[node].setColor(graph['colors'][node])

    def saveGraph(self, filePath):
        #Prepare file
        dictionary = {}
        dictionary['nodes'] = self.numberOfNodes
        dictionary['connections'] = {}
        dictionary['colors'] = {}
        for node in range(self.numberOfNodes):
            dictionary['connections'][node] = self.nodes[node].getConnections()
            dictionary['colors'][node] = self.nodes[node].getColor()

        #save as yaml    
        import yaml
        with open(filePath, 'w') as file:
            yaml.dump(dictionary, file)


    #------------------------------------------#
    # Graph Manipulation (connections, colors) #
    #------------------------------------------#

    #Check if node is already connected if not connect it (no self connections!)
    def addDirectedConnection(self, pickedNode, otherNode):
        if(not otherNode in self.nodes.get(pickedNode).getConnections() and otherNode is not pickedNode):
            self.nodes.get(pickedNode).addConnection(otherNode)

    #performing double Directed connection makes it undirected
    def addUndirectedConnection(self, pickedNode, otherNode):
        self.addDirectedConnection(pickedNode, otherNode)
        self.addDirectedConnection(otherNode, pickedNode)

    def addNode(self):
        self.numberOfNodes+=1
        self.nodes[self.numberOfNodes] = Node()

    def changeNodeColor(self, node, color):
        self.nodes.get(node).setColor(color)

    def getNodeColor(self, node):
        return self.nodes.get(node).getColor()

    def getNodeConnections(self, node):
        return self.nodes.get(node).getConnections()

    #----------#
    # Debuging #
    #----------#
    def ToString(self):
        '''
        Prints graph info (connections, colors)
        '''
        for i in range(len(self.nodes)):
            print(str(i)+":"+self.nodes.get(i).ToString())
