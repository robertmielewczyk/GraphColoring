def plotGraph(graph):
    import networkx as nx
    import matplotlib.pyplot as plt
    G=nx.Graph()

    # Color map
    colorMap = []

    # Add nodes and edges
    for i in range(graph.numberOfNodes):
        G.add_node(i)
        colorMap.append(graph.getNodeColor(i))
        for node in graph.getNodeConnections(i):
            G.add_edge(i, node)

    # Draw Graph
    nx.draw(G, node_color = colorMap, with_labels = True)
    plt.savefig("simple_path.png") # save as png
    plt.show() # display

