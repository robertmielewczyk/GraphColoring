from graphStructure.graph import *
from algorithms.goalFunction import *
from algorithms.naiveSolver import *
from algorithms.hillClimbSolver import *
from debugging.algorithmPlot import *
from debugging.graphPlot import *
from utilities.graphFunctions import *
#------------#
# Show Tasks #
#------------#
def showLoadingSaving():
    # Load Graph from file and display it
    graph = Graph('exampleGraphs/exampleGraph.yaml')
    graph.ToString()

    # Add new connection to graph
    graph.addUndirectedConnection(0,2)

    # Save new graph
    graph.saveGraph('savedGraphs/savedGraph.yaml')

    # Load the new graph and display it
    graph = Graph('savedGraphs/savedGraph.yaml')
    graph.ToString()

def showGoalFunction():
    # Load Graph Example 
    graph = Graph('exampleGraphs/exampleGraph.yaml')

    # Evaluate Score - (used colors, incorrect coloring)
    score = goalFunction(graph)
    print(score)


def showDrawGraph():
    # Load Graph Example
    graph = Graph('exampleGraphs/bigExampleGraph.yaml')

    # Draw
    plotGraph(graph)

def showHillClimb():
    # Load Graph Example 
    graph = Graph('exampleGraphs/bigExampleGraph.yaml')

    # Run Hillclimb
    solver = NaiveSolver(graph)

    #print
    solver.bestGraph.ToString()

    # Draw
    plotGraph(solver.bestGraph)
    
    #Matplot
    plotHistory(solver.history)

def showSaving():
    import pickle
    # Load Graph Example 
    graph = Graph('exampleGraphs/bigExampleGraph.yaml')

    # Run Algorithm
    solver = NaiveSolver(graph)

    # Save Solution
    solver.saveToFile('solution')

def showLoading():
    # Load Solution from File
    solution = loadSolution('solution')

    # Work on solution
    solution.bestGraph.ToString()

def showEverything():
    #showLoadingSaving()
    #showGoalFunction()
    #showDrawGraph()
    showHillClimb()
    #showSaving()
    #showLoading()

showEverything()



    
