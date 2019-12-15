from utilities.graphFunctions import *
from utilities.arrayFunctions import *
from algorithms.goalFunction import *
from graphStructure.graph import *
import copy
class HillClimbSolver():
    def __init__(self, graph):
        self.history = []
        self.bestGraph = Graph()
        self.score = 999999
        self.mask = generateRandomMask(graph)
        self.run(graph, self.mask)

    def run(self, graph, mask):
        # Generate near neighbours +1 -1 (in future update with grasp)
        neighbourSet = generateNeigboursSet(graph, mask)

        # Apply Mask Check Score
        for mask in neighbourSet:
            graph = applyMask(graph, mask)
            newScore = goalFunction(graph)
            if(newScore<self.score):
                self.bestGraph, self.score = copy.deepcopy(graph), newScore
                self.history.append(newScore)
                # Repeat Algorythm
                self.run(graph, mask)

    def saveToFile(self, path):
        import pickle
        with open(path, 'wb') as solution:
            pickle.dump(self, solution)


