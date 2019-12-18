from algorithms.goalFunction import *
from utilities.arrayFunctions import *
from utilities.timer import *
from graphStructure.graph import *
from utilities.graphFunctions import *
from algorithms.algorithm import Algorithm
import time
class NaiveSolver(Algorithm):
    def __init__(self, graph):
        super().__init__()
        self.type = 'Naive'
        self.run(graph)

    def run(self, graph):
        import copy
        start = time.time()
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

        end = time.time()
        self.time = end - start

def calculateFullPropagation(graph):
    end = 0
    base = graph.numberOfNodes
    while((base-1)>0):
        end+=base**(base-1)
        base-=1
    return end
