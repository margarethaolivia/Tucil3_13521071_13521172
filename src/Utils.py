import math

# Representasi simpul yang berisi nomor simpul, nama simpul, dan jalur untuk mencapai simpul tersebut
class NodeUCS :
    def __init__(self,number,distFromRoot,distFromDest,prevPath,name="") :
        self.name = name
        self.number = number
        self.distFromRoot = distFromRoot
        self.distFromDest = distFromDest
        self.prevPath = prevPath
    def __lt__(self,other) :
        return self.distFromRoot < other.distFromRoot

class Graph :
    def readMatrix(fileName) :
        f = open(fileName, "r")
        m = []
        for lines in f.readlines() :
            m.append([int(x) for x in lines.split(' ')])
        f.close()
        return m
    def indexValid(i,mtrx) :
        # checks if index i,j is valid in matrix mtrx
        return (i >= 0 and i < len(mtrx))
    def eucliDistance(x1,y1,x2,y2) :
        return math.sqrt(pow(x2-x1,2) + pow(y2-y1,2))