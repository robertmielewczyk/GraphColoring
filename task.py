import pytest
from graphStructure.graph import Graph
from algorithms.simulatedAnnelingSolver import SimulatedAnnelingSolver

# Load Graph
path = 'exampleGraphs/exampleGraph.yaml'
graph = Graph(path)

solver = SimulatedAnnelingSolver(graph)

print(solver.bestGraph.ToString())