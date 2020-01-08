from utilities.graphFunctions import *
from utilities.arrayFunctions import *
from utilities.timer import *
from algorithms.goalFunction import *
from algorithms.algorithm import Algorithm
from graphStructure.graph import *
import copy
import time
class HillClimbSolver(Algorithm):
    def __init__(self, graph):
        super().__init__()
        self.type = 'HillClimb'
        self.mask = self.generateRandomMask(graph)
        self.run(graph, self.mask)

    def run(self, graph, mask):
        #Start time
        start = time.time()
        # Generate near neighbours +1 -1 (in future update with grasp)
        neighbourSet = generateNeigboursSet(graph, mask)

        # Apply Mask Check Score
        for mask in neighbourSet:
            graph.applyMask(mask)
            newScore = goalFunction(graph)
            if(newScore<self.score):
                self.bestGraph, self.score = copy.deepcopy(graph), newScore
                self.history.append(newScore)
                # Repeat Algorythm
                self.run(graph, mask)
        end = time.time()
        self.time = end - start



