from utilities.graphFunctions import *
from utilities.arrayFunctions import *
from utilities.timer import *
from algorithms.goalFunction import *
from graphStructure.graph import *
import copy
import time
class HillClimbSolver():
    def __init__(self, graph):
        self.type = 'HillClimb'
        self.history = []
        self.bestGraph = Graph()
        self.score = 999999
        self.mask = generateRandomMask(graph)
        self.run(graph, self.mask)

    def run(self, graph, mask):
        #Start time
        start = time.time()
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
        end = time.time()
        self.time = end - start

    def saveToFile(self, path):
        import pickle
        with open(path, 'wb') as solution:
            pickle.dump(self, solution)


