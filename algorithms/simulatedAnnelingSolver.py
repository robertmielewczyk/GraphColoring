from utilities.graphFunctions import *
from utilities.arrayFunctions import *
from utilities.timer import *
from algorithms.goalFunction import *
from graphStructure.graph import *
from utilities.graphFunctions import *
from utilities.arrayFunctions import *
from algorithms.algorithm import Algorithm
import copy
import time
class SimulatedAnnelingSolver(Algorithm):
    def __init__(self, graph, temperature=20, coolingRate=0.003, iterations=1000):
        super().__init__()
        self.type = 'SimulatedAnneling'
        self.mask = generateRandomMask(graph)
        self.run(graph, tabuSize, iterations)

    def run(self, graph, temperature):
        # Initialize
        graph = graph.applyMask(self.mask)
        worse = []

        # Loop until it's too cold
        while(temperature>1):
            for i in range(iterations):
                #Check solution
                if(goalFunction(graph)>goalFunction(self.bestGraph)):
                    self.bestGraph = graph
                newMask = generateNeigboursSet(graph, self.mask)
                #probability = pow(,)


