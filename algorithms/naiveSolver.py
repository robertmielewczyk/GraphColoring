from algorithms.goalFunction import *
from utilities.arrayFunctions import *
from graphStructure.graph import *
from utilities.graphFunctions import *
class NaiveSolver():
    def __init__(self, graph):
        self.history = []
        self.bestGraph = Graph()
        self.score = 999999
        self.__run(graph)

    def __run(self, graph):
        import copy
        '''
        A simple alghorithm that just goes through all nodes and increments colors on them
        until all node reach the color limit:
        Returns:
            -History of scores (mask[0]: score[0])
        '''
        from itertools import product
        # Create color Mask
        mask = [i for i in range(graph.numberOfNodes)]
        end=calculateFullPropagation(graph)

        # Evaluate graph
        for count, i in iter(enumerate(product(mask, repeat=graph.numberOfNodes))):
            if(count > end):
                break
            # Apply mask [0,0,0,...,0] then [0,0,0,...,1] ... [5,5,...,(colorLimit)]
            graph = applyMask(graph, i)

            # Check score for this graph
            score = goalFunction(graph)
            self.history.append(score)
            if(score<self.score):
                self.score, self.bestGraph = score, copy.deepcopy(graph)

    def saveToFile(self, path):
        import pickle
        with open(path, 'wb') as solution:
            pickle.dump(self, solution)


def calculateFullPropagation(graph):
    end = 0
    base = graph.numberOfNodes
    while((base-1)>0):
        end+=base**(base-1)
        base-=1
    return end
