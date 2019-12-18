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