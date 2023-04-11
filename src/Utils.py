import math

# Representasi simpul yang berisi nomor simpul, nama simpul, dan jalur untuk mencapai simpul tersebut
class Node :
    def __init__(self,number,distFromRoot,prevPath,distFromDest=0,name="") :
        self.name = name
        self.number = number
        self.distFromRoot = distFromRoot
        self.distFromDest = distFromDest
        self.prevPath = prevPath

# Fungsi-fungsi yang berhubungan dengan graf
class Util:
    def readMatrix(fileName):
        # Membaca matriks ketetanggan dan koordinat tiap simpul dari file
        f = open(fileName, "r")
        total_lines = len(f.readlines())
        total_nodes = total_lines // 2
        m = []
        coord = []
        f.seek(0)
        lines = f.readlines()
        for i in range(total_nodes):
            m.append([float(x) for x in lines[i].split(' ') if x != ''])

        for i in range(total_nodes, total_lines):
            coord.append([float(x) for x in lines[i].split(' ') if x != ''])

        for i in range(len(m)):
            for j in range(len(m)):
                if m[i][j] != m[j][i]:
                    raise Exception

        f.close()
        print(m)
        return m, coord
    
    def indexValid(i,mtrx) :
        # checks if index i,j is valid in matrix mtrx
        return (i >= 0 and i < len(mtrx))
    
    def eucliDistanceNormal(x1,y1,x2,y2) :
        return math.sqrt(pow(x2*-x1,2) + pow(y2-y1,2))

    def eucliDistanceMap(x1,y1,x2,y2) :
        return math.sqrt(pow(x2*111139-x1*111139,2) + pow(y2*111139-y1*111139,2))
    
    def seperateCoord(fileName) :
        f = open(fileName, 'r')
        lines = f.readlines()
        for i in range(len(lines)) :
            if (i%2 != 0) :
                print(lines[i].rstrip('\n'))
            else :
                print(lines[i].rstrip('\n'), end=" ")

# Util.seperateCoord("D:\\OneDrive - Institut Teknologi Bandung\\Folder Kuliah\\Sem 4\\Stima\\Tucil 3\\Tucil3_13521071_13521172\\test\\koordinat besar.txt")
