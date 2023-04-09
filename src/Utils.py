import math

# Representasi simpul yang berisi nomor simpul, nama simpul, dan jalur untuk mencapai simpul tersebut
class Node :
    def __init__(self,number,distFromRoot,distFromDest,prevPath,name="") :
        self.name = name
        self.number = number
        self.distFromRoot = distFromRoot
        self.distFromDest = distFromDest
        self.prevPath = prevPath

class Graph:
    def readMatrix(fileName):
        f = open(fileName, "r")
        total_lines = len(f.readlines())
        total_nodes = total_lines // 2
        m = []
        coord = []
        f.seek(0)
        lines = f.readlines()
        for i in range(total_nodes):
            m.append([int(x) for x in lines[i].split(' ')])

        for i in range(total_nodes, total_lines):
            coord.append([int(x) for x in lines[i].split(' ')])

        f.close()
        return m, coord
    
    def indexValid(i,mtrx) :
        # checks if index i,j is valid in matrix mtrx
        return (i >= 0 and i < len(mtrx))
    
    def eucliDistanceNormal(x1,y1,x2,y2) :
        return math.sqrt(pow(x2*-x1,2) + pow(y2-y1,2))

    def eucliDistanceMap(x1,y1,x2,y2) :
        return math.sqrt(pow(x2*111139-x1*111139,2) + pow(y2*111139-y1*111139,2))
