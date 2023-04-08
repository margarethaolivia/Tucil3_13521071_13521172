# Representasi simpul yang berisi nomor simpul, nama simpul, dan jalur untuk mencapai simpul tersebut
class Node:
    def __init__(self, number, distFromRoot, distFromDest, prevPath, isUCS, name=""):
        self.name = name
        self.number = number
        self.distFromRoot = distFromRoot
        self.distFromDest = distFromDest
        self.isUCS = isUCS
        self.prevPath = prevPath

    def __lt__(self, other):
        if (self.isUCS):
            return self.distFromRoot < other.distFromRoot
        else:
            return self.distFromRoot + self.distFromDest < other.distFromRoot + other.distFromDest


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
