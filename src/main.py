from Utils import Graph
from AStar import AStar
from UCS import UCS

m, coord = Graph.readMatrix("test/path1.txt")

ucs = UCS(0, 7, m)
astar = AStar(0, 7, m, coord)
