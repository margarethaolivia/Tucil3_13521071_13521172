from queue import PriorityQueue
from Utils import Node
from Utils import Graph

class UCS :
    def __init__(self, startNodeNum, destNodeNum, matrix) :
        liveNodes = PriorityQueue()
        visitedNodesNum = []
        currNode = Node(startNodeNum,0,0,[],True)          # Simpul ekspan
        while (currNode.number != destNodeNum) :
            visitedNodesNum.append(currNode.number)
            for i in range(len(matrix[currNode.number])) : # Masukkan tetangga ke daftar simpul hidup
                if ((i not in visitedNodesNum) and matrix[currNode.number][i] > 0) : # Hanya masukkan simpul yang belum pernah dikunjungi ke daftar simpul hidup
                    liveNodes.put(Node(i, currNode.distFromRoot+matrix[currNode.number][i],
                                       0, currNode.prevPath + [currNode.number], True))
            currNode = liveNodes.get()
        print("---- UCS ALGORITHM ----")
        print(f"Jarak minimum : {currNode.distFromRoot}")
        print("Jalur hasil :",currNode.prevPath+[currNode.number])