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

    def applyMask(self, mask):
        for node in range(self.numberOfNodes):
            self.changeNodeColor(node, mask[node])
        return self

    #----------#
    # Debuging #
    #----------#
    def ToString(self):
        '''
        Prints graph info (connections, colors)
        '''
        for i in range(len(self.nodes)):
            print(str(i)+":"+self.nodes.get(i).ToString())

    def plotGraph(self):
        import networkx as nx
        import matplotlib.pyplot as plt
        G=nx.Graph()
        #disitinct_colors = ['#d90000', '#d96500', '#d9ae00', '#b5d900', '#98d900', '#12d900', '#00d96d', '#00d9a6', '#00d9d2', '#00aed9'\
        #,'#0091d9','#0074d9','#005ad9','#003ad9','#5000d9','#7000d9', '#9400d9', '#b500d9' ,'d900d9', '#d9005a']

        # Color map
        colorMap = [self.getNodeColor(i) for i in range(self.numberOfNodes)]
        nodes = [i for i in range(self.numberOfNodes)]

        # Add nodes and edges
        G.add_nodes_from(nodes)
        for i in range(self.numberOfNodes):
            for node in self.getNodeConnections(i):
                G.add_edge(i, node)
        

        # Draw Graph DEBUG
        #print(f"nodes: {G.nodes}")
        #print(f"edges: {G.edges}")
        #print(f"displayed colors: { {n:c for n,c in zip(G.nodes, colorMap)} } -- If colors dont go in 1,2,3,4 then something is wrong")
        nx.draw_networkx(G, node_color = colorMap, with_labels = True, vmin=0, vmax=self.numberOfNodes)
        plt.savefig("graph_visualised.png") # save as png
        plt.show() # display
