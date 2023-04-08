import osmnx as ox
import networkx as nx
import UCS
import Utils

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

    def search(startCoor, endCoor, mode='walk', method='UCS') :
        # Mengembalikan list koordinat nodes dan graf (untuk keperluan fungsi lain)
        graph = ox.graph_from_point(startCoor,max(int(Utils.Graph.eucliDistance(startCoor[0],startCoor[1],endCoor[0],endCoor[1])), 1000),network_type=mode)
        startNode = ox.distance.nearest_nodes(graph,startCoor[1],startCoor[0])
        endNode = ox.distance.nearest_nodes(graph,endCoor[1],endCoor[0])
        if (method == 'UCS') :
            shortest_route, shortest_distance = UCS.UCSOSMNX.searchPath(startNode, endNode, graph)
        elif(method == 'BuiltIn') :
            shortest_route = nx.shortest_path(graph,startNode,endNode,weight='length')
            shortest_distance = nx.shortest_path_length(graph,startNode,endNode,weight='length')
        return shortest_route, shortest_distance, graph