from Utils import Node
from Utils import Graph
import osmnx as ox

class UCS :
    @staticmethod
    def searchPath(startNodeNum, destNodeNum, matrix) :
        if (not(Graph.indexValid(startNodeNum,matrix)) or not(Graph.indexValid(destNodeNum,matrix))) : # Periksa apakah node valid
            print("Nodes not valid")
            return
        liveNodes = []
        visitedNodesNum = []
        currNode = Node(startNodeNum,0,0,[startNodeNum])          # Simpul ekspan
        while (currNode.number != destNodeNum) :
            visitedNodesNum.append(currNode.number)
            for i in range(len(matrix[currNode.number])) : # Masukkan tetangga ke daftar simpul hidup
                if ((i not in visitedNodesNum) and matrix[currNode.number][i] > 0) : # Hanya masukkan simpul yang belum pernah dikunjungi ke daftar simpul hidup
                    foundSmaller = False
                    for n in liveNodes : # Hapus elemen duplikat yang lebih besar dari elemen skrng dari prioqueue
                        if (n.number == i) :
                            if (currNode.distFromRoot + matrix[currNode.number][i] < n.distFromRoot) :
                                liveNodes.remove(n)
                            else :
                                foundSmaller = True
                            break
                    if (not(foundSmaller)) :
                        liveNodes.append(Node(i, currNode.distFromRoot + matrix[currNode.number][i], 0,
                                        currNode.prevPath + [i]))
            if (len(liveNodes) == 0) : # tidak ada tetangga yang bisa dikunjungi lagi
                return
            liveNodes.sort(key=lambda x : x.distFromRoot)
            currNode = liveNodes[0]
            liveNodes.remove(currNode)
        return currNode.prevPath, currNode.distFromRoot

class UCSOSMNX :
    @staticmethod
    def searchPath(startNode,destNode,graph) :
        # Mencari jalur terpendek berdasarkan panjang 
        if (startNode not in graph or destNode not in graph) :
            print("Coordinate not found in area")
            return
        # Jika simpul mulai sama dengan simpul tujuan
        if (startNode == destNode) :
            return [startNode],0
        liveNodes = []
        visitedNodes = []
        currNode = Node(startNode,0,0,[startNode])
        edges = ox.graph_to_gdfs(graph,nodes=False)
        while (currNode.number != destNode) :
            visitedNodes.append(currNode.number)
            # Cari semua tetangga simpul ekspan
            try :
                neighbour = edges['length'].loc[currNode.number]
            except : # Jika tidak ada tetangga, lanjut ke simpul hidup berikutnya
                if (len(liveNodes) == 0) : # Jika sudah tidak ada simpul hidup dan belum sampai tujuan, berhenti
                    return
                currNode = liveNodes[0]
                liveNodes.remove(currNode)
                continue
            for idx,l in neighbour.items() :
                if ((idx[0]) not in set(visitedNodes)) :
                    foundSmaller = False
                    for n in liveNodes : # Hapus elemen duplikat yang lebih besar dari elemen skrng dari prioqueue, untuk meminimalkan jumlah pencarian
                        if (n.number == idx[0]) :
                            if (currNode.distFromRoot + l < n.distFromRoot) :
                                liveNodes.remove(n)
                            else :
                                foundSmaller = True
                            break
                    if (not(foundSmaller)) :
                        liveNodes.append(Node(idx[0],currNode.distFromRoot + l,0,
                                        currNode.prevPath + [idx[0]]))
            if (len(liveNodes) == 0) :
                return
            liveNodes.sort(key=lambda x : x.distFromRoot)
            currNode = liveNodes[0]
            liveNodes.remove(currNode)
        return currNode.prevPath, currNode.distFromRoot