def goalFunction(graph):
    '''
    Returns a value scoring the solution the smaller the value the better the
    solution Graph is rated on:
        +Number of used colors
        +Ilosc niepoprawnych jeśli zero waga zero inaczej * 5
    '''
    #Generate Score
    score = 0
    score += calculateUsedColors(graph)
    score += calculateGraphColoring(graph)*5
    
    return score

#-----------------------#
# Goal Function Helpers #
#-----------------------#
def calculateGraphColoring(graph):
    incorrect = 0
    for node in range(graph.numberOfNodes):
        adjacentNodes = graph.getNodeConnections(node)
        for adjacentNode in adjacentNodes:
            if(graph.getNodeColor(node) == graph.getNodeColor(adjacentNode)):
                incorrect+=1
    return incorrect

def calculateUsedColors(graph):
    colors = []
    for node in range(graph.numberOfNodes):
        colors.append(graph.getNodeColor(node))
    return countDiffrentNumbersInTuple(colors)

def countDiffrentNumbersInTuple(tupler):
    '''
    function used for true count in graph.usedColors
    alghorithm is ok for this example but terible if tuples would be more disperse
    '''
    count =0 
    end = max(tupler)
    for i in range(end+1):
        if(i in tupler):
            count+=1
    return count