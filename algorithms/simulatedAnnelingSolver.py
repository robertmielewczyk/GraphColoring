from utilities.graphFunctions import *
from utilities.arrayFunctions import *
from utilities.timer import *
from algorithms.goalFunction import *
from graphStructure.graph import *
from utilities.graphFunctions import *
from utilities.arrayFunctions import *
from algorithms.algorithm import Algorithm
import copy
import math
import time
class SimulatedAnnelingSolver(Algorithm):
    def __init__(self, graph, temperature=600, coolingRate=0.95, iterations=50, minTemperature=5):
        super().__init__()
        self.type = 'SimulatedAnneling'
        self.mask = self.generateRandomMask(graph)
        self.run(graph, temperature, coolingRate, minTemperature, iterations)

    def run(self, graph, temperature, coolingRate, minTemperature, iterations):
        start = time.time()
        iteracion = 0
        while(temperature>minTemperature):
            iteracion +=1
            print("Temperature: {}/{}".format(int(temperature), minTemperature))
            for i in range(iterations):
                newMask = self.neighbour(graph, self.mask)
                graph.applyMask(newMask)
                newScore = goalFunction(graph)

                if(newScore<self.score):
                    self.mask = newMask
                    self.score = newScore
                    self.bestGraph = copy.deepcopy(graph)
                    self.history.append(self.score)

                #Simulated annealing prob
                if(random.random()<self.prob(temperature, self.score, newScore)):
                    self.mask = newMask

            #Lower Temperature
            temperature *= coolingRate 
        end = time.time()
        self.time = end - start


    def neighbour(self, graph, mask):
        '''/* Different neighbor selection strategies: 
        * Move all points 0 or 1 units in a random direction 
        * Shift input elements randomly 
        * Swap random elements in input sequence 
        * Permute input sequence 
        * Partition input sequence into a random number 
          of segments and permute segments   */
        '''
        neighbour_set = generateNeigboursSet(graph, mask)
        return neighbour_set[random.randrange(0,len(neighbour_set)-1)]

    def prob(self, temperature, score, newScore):
        return math.exp(-(score-newScore)/temperature)



