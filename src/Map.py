import osmnx as ox
import networkx as nx
import UCS
import Utils
import AStar

ox.settings.log_console=True
ox.settings.use_cache=True

class MapPathSearch :
    def convertPathToCoorPath(nodePath,graph) :
        # Mengubah path node menjadi path koordinat
        coorPath = []
        nodes = ox.graph_to_gdfs(graph,edges=False)
        for n in nodePath :
            nodeData = nodes.loc[n]
            coorPath.append((nodeData['y'],nodeData['x']))
        return coorPath

    def search(startCoor, endCoor, method, mode='walk') :
        # Mengembalikan list koordinat nodes dan graf (untuk keperluan fungsi lain)
        mapping_distance = max(int(Utils.Graph.eucliDistanceMap(startCoor[0],startCoor[1],endCoor[0],endCoor[1])), 1000)
        if (mapping_distance > 1000) :
            graph = ox.graph_from_point(startCoor, mapping_distance, network_type='drive')
        else :
            graph = ox.graph_from_point(startCoor, mapping_distance, network_type=mode)
        startNode = ox.distance.nearest_nodes(graph,startCoor[1],startCoor[0])
        endNode = ox.distance.nearest_nodes(graph,endCoor[1],endCoor[0])
        try :
            if (method == 'UCS') :
                shortest_route, shortest_distance = UCS.UCSOSMNX.searchPath(startNode, endNode, graph)
            elif(method == 'A*') :
                shortest_route, shortest_distance = AStar.AStarOSMNX.searchPath(startNode, endNode, graph)
        except :
            return -1,-1,None,False
        return shortest_route, shortest_distance, graph, True