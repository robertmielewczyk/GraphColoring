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
        self.total_end=0
        self.total =0
        self.run(graph, self.mask)

    def run(self, graph, mask):
        #Start time
        start = time.time()
        # Generate near neighbours +1 -1 (in future update with grasp)
        neighbourSet = generateNeigboursSet(graph, mask)

        # Apply Mask Check Score
        for count ,mask in enumerate(neighbourSet):
            print("Aplying mask: {}/{} : {}/{}".format(count, len(neighbourSet), self.total, self.total_end))
            graph.applyMask(mask)
            newScore = goalFunction(graph)
            if(newScore<self.score):
                print("Found a better solution: {} --> generating new neighbours".format(newScore))
                self.bestGraph, self.score = copy.deepcopy(graph), newScore
                self.history.append(newScore)
                # Repeat Algorythm
                self.total_end+=1
                self.run(graph, mask)
            # Debug
            if(count==len(neighbourSet)-1):
                self.total+=1
        end = time.time()
        self.time = end - start



