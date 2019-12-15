from utilities.graphFunctions import *
from utilities.arrayFunctions import *
from algorithms.goalFunction import *
from graphStructure.graph import *
import copy
class TabuSolver():
    def __init__(self, graph, tabuSize=5, iterations=1000):
        self.history = []
        self.bestGraph = Graph()
        self.score = 999999
        self.mask = generateRandomMask(graph)
        self.run(graph, tabuSize, iterations)

    def run(self, graph, tabuSize, iterations):
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
        self.bestGraph = applyMask(graph, self.mask)
        self.score = goalFunction(self.bestGraph)


                
    def saveToFile(self, path):
        import pickle
        with open(path, 'wb') as solution:
            pickle.dump(self, solution)