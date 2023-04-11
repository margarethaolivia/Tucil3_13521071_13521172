import osmnx as ox
import UCS
import Utils
import AStar

ox.settings.use_cache=True

class MapPathSearch :
    savedGraph = None
    boundBox = []

    def saveGraphFile(fileName) :
        # Membaca graf dari file xml
        MapPathSearch.savedGraph = ox.graph_from_xml(fileName)
        MapPathSearch.boundBox = ox.graph_to_gdfs(MapPathSearch.savedGraph, edges=False).total_bounds
        center = ((MapPathSearch.boundBox[0] + MapPathSearch.boundBox[2])/2, (MapPathSearch.boundBox[1] + MapPathSearch.boundBox[3])/2)
        # nodesList = ox.graph_to_gdfs(MapPathSearch.savedGraph, edges=False).values
        # coordList = []
        # for n in nodesList :
        #     coordList.append((n[0],n[1]))
        return center #, coordList
    
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
        nodes = ox.graph_to_gdfs(graph,edges=False)
        for n in nodePath :
            nodeData = nodes.loc[n]
            coorPath.append((nodeData['y'],nodeData['x']))
        return coorPath
    
    def isInBoundBox(coor) :
        # Memeriksa apakah coor ada di dalam bounding box
        if (not(any(MapPathSearch.boundBox))) :
            return False
        elif (coor[0] < MapPathSearch.boundBox[0] or coor[0] > MapPathSearch.boundBox[2]
            or coor[1] < MapPathSearch.boundBox[1] or coor[1] > MapPathSearch.boundBox[3]) :
            return False
        return True

    def search(startCoor, endCoor, method) :
        # Mengembalikan list koordinat nodes dan graf (untuk keperluan fungsi lain)
        if (not(MapPathSearch.isInBoundBox(startCoor)) or not(MapPathSearch.isInBoundBox(endCoor))) :
            print("Generating new graph")
            MapPathSearch.saveGraphPoint(startCoor, endCoor)
        startNode = ox.distance.nearest_nodes(MapPathSearch.savedGraph,startCoor[0],startCoor[1])
        endNode = ox.distance.nearest_nodes(MapPathSearch.savedGraph,endCoor[0],endCoor[1])
        try :
            if (method == 'UCS') :
                shortest_route, shortest_distance = UCS.UCSOSMNX.searchPath(startNode, endNode, MapPathSearch.savedGraph)
            elif(method == 'A*') :
                shortest_route, shortest_distance = AStar.AStarOSMNX.searchPath(startNode, endNode, MapPathSearch.savedGraph)
        except :
            return -1,-1,None,False
        return shortest_route, shortest_distance, MapPathSearch.savedGraph, True