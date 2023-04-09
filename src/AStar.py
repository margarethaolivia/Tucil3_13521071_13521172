from Utils import Node
from Utils import Graph
import math


class AStar:
    @staticmethod
    def searchPath(startNodeNum, destNodeNum, matrix, coord):
        if (not(Graph.indexValid(startNodeNum,matrix)) or not(Graph.indexValid(destNodeNum,matrix))) : # Periksa apakah node valid
            print("Nodes not valid")
            return
        liveNodes = []
        visitedNodesNum = []
        startCoord = coord[startNodeNum]
        destCoord = coord[destNodeNum]
        currNode = Node(startNodeNum, 0, AStar.euc_dist(
            startCoord, destCoord), [])          # Simpul ekspan
        while (currNode.number != destNodeNum):
            visitedNodesNum.append(currNode.number)
            # Masukkan tetangga ke daftar simpul hidup
            for i in range(len(matrix[currNode.number])):
                # Hanya masukkan simpul yang belum pernah dikunjungi ke daftar simpul hidup
                if ((i not in visitedNodesNum) and matrix[currNode.number][i] > 0):
                    liveNodes.append(Node(i, currNode.distFromRoot+matrix[currNode.number][i],
                                       AStar.euc_dist(coord[currNode.number], destCoord), currNode.prevPath + [currNode.number]))
            if (len(liveNodes) == 0) : # tidak ada tetangga yang bisa dikunjungi lagi
                return
            liveNodes.sort(key=lambda x : x.distFromRoot+x.distFromDest)
            currNode = liveNodes[0]
            liveNodes.remove(currNode)
        return currNode.prevPath, currNode.distFromRoot

    @staticmethod
    def euc_dist(self, point1, point2):
        return math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)
