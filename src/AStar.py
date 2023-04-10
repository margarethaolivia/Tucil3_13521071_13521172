from Utils import Node
import math
import osmnx as ox

class AStar:
    @staticmethod
    def searchPath(startNodeNum, destNodeNum, matrix, coord):
        liveNodes = []
        visitedNodesNum = []
        startCoord = coord[startNodeNum]
        destCoord = coord[destNodeNum]
        currNode = Node(startNodeNum, 0, AStar.euc_dist(
            startCoord, destCoord), [startNodeNum])          # Simpul ekspan
        while (currNode.number != destNodeNum):
            visitedNodesNum.append(currNode.number)
            # Masukkan tetangga ke daftar simpul hidup
            for i in range(len(matrix[currNode.number])):
                # Hanya masukkan simpul yang belum pernah dikunjungi ke daftar simpul hidup
                if ((i not in visitedNodesNum) and matrix[currNode.number][i] > 0):
                    liveNodes.append(Node(i, currNode.distFromRoot+matrix[currNode.number][i],
                                       AStar.euc_dist(coord[i], destCoord), currNode.prevPath + [i]))
            if (len(liveNodes) == 0) : # tidak ada tetangga yang bisa dikunjungi lagi
                return
            liveNodes.sort(key=lambda x : x.distFromRoot+x.distFromDest)
            currNode = liveNodes[0]
            liveNodes.remove(currNode)
        return currNode.prevPath, currNode.distFromRoot

    @staticmethod
    def euc_dist(point1, point2):
        return math.sqrt((point2[0]-point1[0])**2 + (point2[1]-point1[1])**2)

class AStarOSMNX :
    @staticmethod
    def searchPath(startNode, destNode, graph):
        # Mencari jalur terpendek berdasarkan panjang 
        if (startNode not in graph or destNode not in graph) :
            print("Coordinate not found in area")
            return
        liveNodes = []
        visitedNodes= []
        nodes,edges = ox.graph_to_gdfs(graph)
        coord = (nodes['x'], nodes['y'])
        startCoord = (coord[0].loc[startNode], coord[1].loc[startNode])
        destCoord = (coord[0].loc[destNode], coord[1].loc[destNode])
        currNode = Node(startNode, 0, AStar.euc_dist(
            startCoord, destCoord), [startNode])          # Simpul ekspan
        while (currNode.number != destNode):
            visitedNodes.append(currNode.number)
            # Cari semua tetangga simpul ekspan
            try :
                neighbour = edges['length'].loc[currNode.number]
            except : # Jika tidak ada tetangga, lanjut
                if (len(liveNodes) == 0) : # Jika sudah tidak ada simpul hidup dan belum sampai tujuan, berhenti
                    return
                currNode = liveNodes[0]
                liveNodes.remove(currNode)
                continue
            # Masukkan tetangga ke daftar simpul hidup
            for idx,l in neighbour.items() :
                if ((idx[0]) not in set(visitedNodes)) :
                    liveNodes.append(Node(idx[0], currNode.distFromRoot+l,
                                       AStar.euc_dist((coord[0].loc[idx[0]],coord[1].loc[idx[0]]), destCoord), 
                                       currNode.prevPath + [idx[0]]))
            if (len(liveNodes) == 0) : # tidak ada tetangga yang bisa dikunjungi lagi
                return
            liveNodes.sort(key=lambda x : x.distFromRoot+x.distFromDest)
            currNode = liveNodes[0]
            liveNodes.remove(currNode)
        return currNode.prevPath, currNode.distFromRoot