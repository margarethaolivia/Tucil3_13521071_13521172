import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from Utils import Graph


def plotGraph(m, coord):
    adj_matrix = np.array(m)

    # Create a directed weighted graph from the weighted directed adjacency matrix
    graph = nx.Graph(adj_matrix)

    # Plot the directed weighted graph
    pos = {i: tuple(coord[i]) for i in range(len(coord))}

    # Draw graph with fixed node positions and edge labels
    nx.draw_networkx(graph, pos=pos, with_labels=True, node_color='lightblue',
                     node_size=500, font_size=14, font_weight='bold')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={(
        i, j): f'{adj_matrix[i, j]:.1f}' for i, j in graph.edges()}, font_size=12, font_color='red')
    plt.axis('off')
    plt.show()
