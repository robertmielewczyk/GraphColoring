from abc import ABC,abstractmethod 
from graphStructure.graph import *
class Algorithm(ABC):
    def __init__(self):
        self.history = []
        self.bestGraph = Graph()
        self.score = 999999

    @abstractmethod
    def run(self):
        pass

    def saveToFile(self, path):
        import pickle
        with open(path, 'wb') as solution:
            pickle.dump(self, solution)

    def generateRandomMask(self, graph):
        import random
        maxColors = graph.numberOfNodes-1
        mask = [random.randint(0, maxColors) for i in range(graph.numberOfNodes)]
        return mask

    def plotHistory(self):
        # Plot History
        import matplotlib.pyplot as plt
        plt.plot(self.history)
        plt.ylabel('score')
        plt.xlabel('sample')
        plt.show()