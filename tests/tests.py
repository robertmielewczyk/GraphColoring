import pytest
import sys
sys.path.append('.')
from graphStructure.graph import Graph
from algorithms.naiveSolver import NaiveSolver
from algorithms.hillClimbSolver import HillClimbSolver
from algorithms.tabuSolver import TabuSolver
from algorithms.simulatedAnnelingSolver import SimulatedAnnelingSolver
from algorithms.geneticSolver import GeneticSolver

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
    assert(solver.score<=graph.numberOfNodes)

    # Test HillClimb
    solver = HillClimbSolver(graph)
    assert(solver.score<=graph.numberOfNodes*6)

    # Test Tabu
    solver = TabuSolver(graph)
    assert(solver.score<=graph.numberOfNodes*6)

    # Test Simulated Anneling
    solver = SimulatedAnnelingSolver(graph)
    assert(solver.score<=graph.numberOfNodes*6)

    # Test Genetic Algorithm
    params = {}
    params['population'] = 10
    params['generations'] = 10
    params['avg_tresh'] = 10
    params['deviation_tresh'] = 10
    params['succesion'] = "Tournament"
    params['termination'] = "Iter"
    params['cross_prob'] = 1
    params['mutation_prob'] = 1
    solver = GeneticSolver(graph, params=params)

def test_experiments():
    pass



