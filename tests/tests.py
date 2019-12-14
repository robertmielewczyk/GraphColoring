import pytest
from graphStructure.graph import Graph
def test_graph():
    # Load Graph
    path = 'exampleGraphs/exampleGraph.yaml'
    graph = Graph(path)