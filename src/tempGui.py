import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

# Example weighted adjacency matrix with direction
W = np.array([[0, 0.5, 0.2, 0],
              [0.5, 0, 0.7, 0.8],
              [0.2, 0.7, 0, 0.9],
              [0, 0.8, 0.9, 0]])

# Create directed graph from adjacency matrix
G = nx.Graph(W)

# Define node positions as a 2D matrix
pos_matrix = np.array([[1, 2], [3, 4], [1, 8], [7, 8]])

# Convert 2D matrix to dictionary of node positions
pos = {i: tuple(pos_matrix[i]) for i in range(len(pos_matrix))}

result = [0, 1, 3]

path_edges = []
for i in range(len(result)-1):
    path_edges.append(tuple((result[i], result[i+1])))

# Draw graph with fixed node positions and edge labels
nx.draw_networkx(G, pos=pos, with_labels=True, node_color=['blue' if e in result else 'lightblue' for e in G.nodes()],
                 node_size=500, font_size=14, font_weight='bold',
                 edge_color=['blue' if e in path_edges else 'black' for e in G.edges()])
nx.draw_networkx_edge_labels(G, pos, edge_labels={(
    i, j): f'{W[i, j]:.1f}' for i, j in G.edges()}, font_size=12, font_color='red')
plt.axis('off')
plt.show()
