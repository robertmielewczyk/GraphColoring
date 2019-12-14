import pytest
from graphStructure.graph import *
def test_graph():
    # Load Graph from path
    path = "exampleGraphs/exampleGraph.yaml"
    graph = Graph(path)

