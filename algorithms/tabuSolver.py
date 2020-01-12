from utilities.graphFunctions import *
from utilities.arrayFunctions import *
from utilities.timer import *
from algorithms.goalFunction import *
from graphStructure.graph import *
from algorithms.algorithm import Algorithm
import copy
import time
class TabuSolver(Algorithm):
    def __init__(self, graph, tabuSize=5, iterations=1000):
        super().__init__()
        self.type = 'Tabu'
        self.mask = self.generateRandomMask(graph)
        self.run(graph, tabuSize, iterations)

    def run(self, graph, tabuSize, iterations):
        start = time.time()
        # Tabu setup
        # Generate random solution
        bestMask = self.mask
        tabuList = []
        tabuList.append(self.mask)
        index=0
        while(index!=iterations):
            index+=1
            # Generate near neighbours
            neighbourMasks = generateNeigboursSet(graph, bestMask) #Neighbour masks include initial mask
            
            # Tabu
            # Check all near neighbours
            for neighbourMask in neighbourMasks:
                graph.applyMask(neighbourMask)
                score = goalFunction(graph)
                graph.applyMask(bestMask)
                bestMaskScore = goalFunction(graph)
                # If there is a better neighbour than current solution update it
                if(neighbourMask not in tabuList and score<bestMaskScore):
                    bestMask = neighbourMask
            # If better solution was found than initial solution
            # Update it
            if(goalFunction(graph.applyMask(bestMask))<goalFunction(graph.applyMask(self.mask))): 
                self.mask = bestMask
                self.history.append(goalFunction(graph.applyMask(self.mask))) #ugly
            # Add best previous solution search to tabu list
            tabuList.append(bestMask)

            # Delete first element from Tabu list
            if(len(tabuList)>tabuSize):
                del tabuList[0]

        #self.mask is the best output
        self.bestGraph = graph.applyMask(self.mask)
        self.score = goalFunction(self.bestGraph)

        end = time.time()
        self.time = end - start
        print(self.time)
