def applyMask(graph, mask):
    # Apply mask
    for node in range(graph.numberOfNodes):
        graph.changeNodeColor(node, mask[node])
    return graph

def generateRandomMask(graph):
    import random
    maxColors = graph.numberOfNodes-1
    mask = [random.randint(0, maxColors) for i in range(graph.numberOfNodes)]
    return mask

def loadSolution(solutionPath):
    import pickle
    with open(solutionPath, 'rb') as solution:
        return pickle.load(solution)