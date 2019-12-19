def loadSolution(solutionPath):
    import pickle
    with open(solutionPath, 'rb') as solution:
        return pickle.load(solution)