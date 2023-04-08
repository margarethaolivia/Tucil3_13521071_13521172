from queue import PriorityQueue
from Utils import Node
from Utils import Graph
import math


class AStar:
    def __init__(self, startNodeNum, destNodeNum, matrix, coord):
        liveNodes = PriorityQueue()
        visitedNodesNum = []
        startCoord = coord[startNodeNum]
        destCoord = coord[destNodeNum]
        currNode = Node(startNodeNum, 0, self.euc_dist(
            startCoord, destCoord), [], False)          # Simpul ekspan
        while (currNode.number != destNodeNum):
            visitedNodesNum.append(currNode.number)
            # Masukkan tetangga ke daftar simpul hidup
            for i in range(len(matrix[currNode.number])):
                # Hanya masukkan simpul yang belum pernah dikunjungi ke daftar simpul hidup
                if ((i not in visitedNodesNum) and matrix[currNode.number][i] > 0):
                    liveNodes.put(Node(i, currNode.distFromRoot+matrix[currNode.number][i],
                                       self.euc_dist(coord[currNode.number], destCoord), currNode.prevPath + [currNode.number], False))
            currNode = liveNodes.get()
        print("---- A* ALGORITHM ----")
        print(f"Jarak minimum : {currNode.distFromRoot}")
        print("Jalur hasil :", currNode.prevPath+[currNode.number])

    def euc_dist(self, point1, point2):
        return math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
