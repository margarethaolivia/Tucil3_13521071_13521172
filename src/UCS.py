from Utils import Node
import osmnx as ox

class UCS :
    @staticmethod
    def searchPath(startNodeNum, destNodeNum, matrix) :
        # Route searching pada matriks ketetanggaan
        liveNodes = []
        visitedNodesNum = []
        currNode = Node(startNodeNum,0,[startNodeNum])          # Simpul ekspan
        while (currNode.number != destNodeNum) :
            visitedNodesNum.append(currNode.number)
            for i in range(len(matrix[currNode.number])) : # Masukkan tetangga ke daftar simpul hidup
                if ((i not in visitedNodesNum) and matrix[currNode.number][i] > 0) : # Hanya masukkan simpul yang belum pernah dikunjungi ke daftar simpul hidup
                    liveNodes.append(Node(i, currNode.distFromRoot + matrix[currNode.number][i],
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
        # Route searching pada graf osmnx
        # Mencari jalur terpendek berdasarkan panjang jalan
        if (startNode == destNode) : # Jika simpul mulai sama dengan simpul tujuan
            return [startNode],0
        liveNodes = []
        visitedNodes = []
        currNode = Node(startNode,0,[startNode])
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
                    liveNodes.append(Node(idx[0],currNode.distFromRoot + l,
                                    currNode.prevPath + [idx[0]]))
            if (len(liveNodes) == 0) :
                return
            liveNodes.sort(key=lambda x : x.distFromRoot)
            currNode = liveNodes[0]
            liveNodes.remove(currNode)
        return currNode.prevPath, currNode.distFromRoot