from queue import PriorityQueue
from Utils import NodeUCS
from Utils import Graph
import osmnx as ox

class UCS :
    def __init__(self, startNodeNum, destNodeNum, matrix) :
        if (not(Graph.indexValid(startNodeNum,matrix)) or not(Graph.indexValid(destNodeNum,matrix))) : # Periksa apakah node valid
            print("Nodes not valid")
            return
        liveNodes = []
        visitedNodesNum = []
        currNode = NodeUCS(startNodeNum,0,0,[startNodeNum])          # Simpul ekspan
        while (currNode.number != destNodeNum) :
            visitedNodesNum.append(currNode.number)
            for i in range(len(matrix[currNode.number])) : # Masukkan tetangga ke daftar simpul hidup
                if ((i not in visitedNodesNum) and matrix[currNode.number][i] > 0) : # Hanya masukkan simpul yang belum pernah dikunjungi ke daftar simpul hidup
                    foundSmaller = False
                    if i in liveNodes : # Hapus elemen duplikat yang lebih besar dari elemen skrng dari prioqueue
                        liveNodes.remove(i)
                    if (not(foundSmaller)) :
                        liveNodes.append(NodeUCS(i,currNode.distFromRoot + matrix[currNode.number][i],0,
                                        currNode.prevPath + [i]))
            liveNodes.sort(key=lambda x : x.distFromRoot)
            currNode = liveNodes[0]
            liveNodes.remove(currNode)
        print(f"Jarak minimum : {currNode.distFromRoot}")
        print("Jalur hasil :",currNode.prevPath)

class UCSOSMNX :
    @staticmethod
    def searchPath(startNode,destNode,graph) :
        # Mencari jalur terpendek berdasarkan panjang 
        if (startNode not in graph or destNode not in graph) :
            print("Coordinate not found in area")
        else :
            if (startNode == destNode) :
                return [startNode],0
            liveNodes = []
            visitedNodes = []
            currNode = NodeUCS(startNode,0,0,[startNode])
            edges = ox.graph_to_gdfs(graph,nodes=False)
            while (currNode.number != destNode) :
                visitedNodes.append(currNode.number)
                neighbour = edges['length'].loc[currNode.number]
                for idx,l in neighbour.items() :
                    if ((idx[0]) not in set(visitedNodes)) :
                        foundSmaller = False
                        for n in liveNodes : # Hapus elemen duplikat yang lebih besar dari elemen skrng dari prioqueue
                            if (n.number == idx[0]) :
                                if (currNode.distFromRoot + l < n.distFromRoot) :
                                    liveNodes.remove(n)
                                else :
                                    foundSmaller = True
                                break
                        if (not(foundSmaller)) :
                            liveNodes.append(NodeUCS(idx[0],currNode.distFromRoot + l,0,
                                            currNode.prevPath + [idx[0]]))
                liveNodes.sort(key=lambda x : x.distFromRoot)
                currNode = liveNodes[0]
                liveNodes.remove(currNode)
            return currNode.prevPath, currNode.distFromRoot

# m = Graph.readMatrix("D:\OneDrive - Institut Teknologi Bandung\Folder Kuliah\Sem 4\Stima\Tucil 3\Tucil3_13521071_13521172\doc\dummy.txt")
# a = UCS(0,6,m)