from utilities.graphFunctions import *
from utilities.arrayFunctions import *
from utilities.timer import *
from algorithms.goalFunction import *
from algorithms.algorithm import Algorithm
from graphStructure.graph import *
import copy
import time
class HillClimbShallowSolver(Algorithm):
    def __init__(self, graph, iterations):
        super().__init__()
        self.type = 'HillClimb'
        self.mask = self.generateRandomMask(graph)
        self.run(graph, self.mask, iterations)

    def run(self, graph, mask, iterations=100):
        #Start time
        start = time.time()
        for i in range(iterations):
            # Generate near neighbours +1 -1 (in future update with grasp)
            neighbourSet = generateNeigboursSet(graph, mask)
            mask = neighbourSet[random.randrange(0,len(neighbourSet)-1)]

            # Apply Mask Check Score
            graph.applyMask(mask)
            newScore = goalFunction(graph)
            if(newScore<self.score):
                self.bestGraph, self.score = copy.deepcopy(graph), newScore
                self.history.append(newScore)
            
        end = time.time()
        self.time = end - start



