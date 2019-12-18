import pytest
from graphStructure.graph import Graph
from algorithms.naiveSolver import NaiveSolver
from algorithms.hillClimbSolver import HillClimbSolver
from algorithms.tabuSolver import TabuSolver

def test_graph():
    # Load Graph
    path = 'exampleGraphs/exampleGraph.yaml'
    graph = Graph(path)

def test_algorithms():
    # Load Graph
    path = 'exampleGraphs/exampleGraph.yaml'
    graph = Graph(path)

    # Test Naive
    solver = NaiveSolver(graph)

    # Test HillClimb
    solver = HillClimbSolver(graph)

    # Test Tabu
    solver = TabuSolver(graph)



