from utilities import *
class GraphSort():
    def returnColloredGraphs(self, graphs, colored):
        '''
        return either correctly colored or incorrectly colored graphs
        '''
        array = []
        for graph in graphs:
            if(graph.isCorrectlyColored == colored):
                array.append(graph)
        return array

    def returnUsedColors(self, graphs, usedColors):
        array = []
        for graph in graphs:
            if(graph.usedColors == usedColors):
                array.append(graph)
        return array

    def returnMinColorUse(self, graphs):
        graphs = self.returnColloredGraphs(graphs, True)
        minimum = 999999
        for graph in graphs:
            if(graph.usedColors < minimum):
                minimum = graph.usedColors
        return self.returnUsedColors(graphs, minimum)

    def returnMaxColorUse(self):
        pass

    def returnUsedColorRange(self, graphs, minimum, maximum):
        array = []
        for graph in graphs:
            if(graph.usedColors >= minimum or graph.usedColors <= maximum):
                array.append(graph)
        return array