import osmnx as ox
import networkx as nx
import numpy as np
import UCS
import Utils
import AStar

ox.settings.use_cache=False

class MapPathSearch :
    savedGraph = None
    boundBox = []
    mat = None
    graphCoords = None

    def saveGraphFile(fileName) :
        # Membaca graf peta dari file txt berisi matriks ketetanggan, koordinat, dan nama
        MapPathSearch.mat,MapPathSearch.graphCoords,names = Utils.Util.readMatrix(fileName)
        adj_matrix = np.array(MapPathSearch.mat)
        MapPathSearch.savedGraph = nx.Graph(adj_matrix)
        nx.set_node_attributes(MapPathSearch.savedGraph, {"x" : 0, "y" : 0})
        for i in range(len(MapPathSearch.savedGraph.nodes)) :
            MapPathSearch.savedGraph.nodes[i]["x"] = MapPathSearch.graphCoords[i][0]
            MapPathSearch.savedGraph.nodes[i]["y"] = MapPathSearch.graphCoords[i][1]
        edgeList = [] # Penampung koordinat tiap rusuk
        for u,v in MapPathSearch.savedGraph.edges :
            edgeList.append([(MapPathSearch.savedGraph.nodes[u]["y"], MapPathSearch.savedGraph.nodes[u]["x"]),
                             (MapPathSearch.savedGraph.nodes[v]["y"], MapPathSearch.savedGraph.nodes[v]["x"])])
        minX = MapPathSearch.graphCoords[0][0]
        minY = MapPathSearch.graphCoords[0][1]
        maxX = MapPathSearch.graphCoords[0][0]
        maxY = MapPathSearch.graphCoords[0][1]
        for c in MapPathSearch.graphCoords :
            if (c[0] < minX) :
                minX = c[0]
            elif (c[0] > maxX) :
                maxX = c[0]
            if (c[1] < minY) :
                minY = c[1]
            elif (c[1] > maxY) :
                maxY = c[1]
        MapPathSearch.boundBox = [minX, minY, maxX, maxY]
        center = ((MapPathSearch.boundBox[0] + MapPathSearch.boundBox[2])/2, (MapPathSearch.boundBox[1] + MapPathSearch.boundBox[3])/2)
        return center, MapPathSearch.graphCoords, names, edgeList
    
    def saveGraphPoint(start, end) :
        # Download graph berdasarkan bounding box start,end
        dist = Utils.Util.eucliDistanceMap(start[0],start[1],end[0],end[1])
        if (dist > 1000) : # Jika jarak > 1 km, cari jalur yang bisa dilalui kendaraan saja
            MapPathSearch.savedGraph = ox.graph_from_bbox(max(start[1],end[1]) + 0.001, min(start[1],end[1])-0.001, max(start[0],end[0]) + 0.001, min(start[0],end[0])-0.001,
                                                           network_type='drive')
        else :
            MapPathSearch.savedGraph = ox.graph_from_bbox(max(start[1],end[1]) + 0.001, min(start[1],end[1])-0.001, max(start[0],end[0]) + 0.001, min(start[0],end[0])-0.001,
                                                           network_type='walk')
        MapPathSearch.boundBox = ox.graph_to_gdfs(MapPathSearch.savedGraph, edges=False).total_bounds

    def convertPathToCoorPath(nodePath,graph) :
        # Mengubah path node menjadi path koordinat
        coorPath = []
        try :
            # Graf osmnx
            nodes = ox.graph_to_gdfs(graph,edges=False)
            for n in nodePath :
                nodeData = nodes.loc[n]
                coorPath.append((nodeData['y'],nodeData['x']))
        except :
            # Graf nx
            for n in nodePath :
                coorPath.append((graph.nodes[n]['y'],graph.nodes[n]['x']))
        return coorPath
    
    def searchClosestNode(graph,coor) :
        # Mencari koordinat terdekat untuk graf nx biasa
        if (graph == None) :
            return
        closestNode = graph.nodes[0]
        closestIdx = 0
        for i in range(len(graph.nodes)) :
            if (Utils.Util.eucliDistanceMap(graph.nodes[i]['x'], graph.nodes[i]['y'],coor[0],coor[1]) <
                Utils.Util.eucliDistanceMap(closestNode['x'],closestNode['y'],coor[0],coor[1])) :
                closestNode = graph.nodes[i]
                closestIdx = i
        return closestIdx

    def isInBoundBox(coor) :
        # Memeriksa apakah coor ada di dalam bounding box
        if (len(MapPathSearch.boundBox) == 0) :
            return False
        elif (coor[0] < MapPathSearch.boundBox[0] or coor[0] > MapPathSearch.boundBox[2]
            or coor[1] < MapPathSearch.boundBox[1] or coor[1] > MapPathSearch.boundBox[3]) :
            return False
        return True

    def search(startCoor, endCoor, method) :
        # Mengembalikan list koordinat nodes dan graf (untuk keperluan fungsi lain)
        if (not(MapPathSearch.isInBoundBox(startCoor)) or not(MapPathSearch.isInBoundBox(endCoor))) :
            # Jika koordinat ada di luar graf, buat graf baru
            MapPathSearch.saveGraphPoint(startCoor, endCoor)
        try :
            isOSMGraph = True
            startNode = ox.distance.nearest_nodes(MapPathSearch.savedGraph,startCoor[0],startCoor[1])
            endNode = ox.distance.nearest_nodes(MapPathSearch.savedGraph,endCoor[0],endCoor[1])
        except :
            isOSMGraph = False
            startNode = MapPathSearch.searchClosestNode(MapPathSearch.savedGraph,startCoor)
            endNode = MapPathSearch.searchClosestNode(MapPathSearch.savedGraph,endCoor)
        try :
            if (isOSMGraph) :
                if (method == 'UCS') :
                    shortest_route, shortest_distance = UCS.UCSOSMNX.searchPath(startNode, endNode, MapPathSearch.savedGraph)
                elif(method == 'A*') :
                    shortest_route, shortest_distance = AStar.AStarOSMNX.searchPath(startNode, endNode, MapPathSearch.savedGraph)
            else : # Graf nx biasa
                if (method == 'UCS') :
                    shortest_route, shortest_distance = UCS.UCS.searchPath(startNode, endNode, MapPathSearch.mat)
                elif(method == 'A*') :
                    shortest_route, shortest_distance = AStar.AStar.searchPath(startNode, endNode, MapPathSearch.mat, MapPathSearch.graphCoords)
        except : # Gagal
            return -1,-1,None,False
        return shortest_route, shortest_distance, MapPathSearch.savedGraph, True