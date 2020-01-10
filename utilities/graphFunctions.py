# import only system from os 
from os import system, name 
def loadSolution(solutionPath):
    import pickle
    with open(solutionPath, 'rb') as solution:
        return pickle.load(solution)