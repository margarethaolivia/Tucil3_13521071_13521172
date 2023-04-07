import osmnx as ox
import networkx as nx
import UCS
import matplotlib as plt

ox.settings.log_console=True
ox.settings.use_cache=True
# define the start and end locations in latlng
start_latlng = (1000,10000)
end_latlng = (-1000,-900)
# location where you want to find your route
place     = 'San Francisco, California, United States'
# find shortest route based on the mode of travel
mode      = 'walk'        # 'drive', 'bike', 'walk'
# find shortest path based on distance or time
optimizer = 'length'        # 'length','time'
# create graph from OSM within the boundaries of some 
# geocodable place(s)
graph = ox.graph_from_place(place, network_type = mode)
# find the nearest node to the start location
orig_node = ox.distance.nearest_nodes(graph, start_latlng[1],
                                      start_latlng[0])
# find the nearest node to the end location
dest_node = ox.distance.nearest_nodes(graph, end_latlng[1],
                                      end_latlng[0])

print(orig_node)
print(dest_node)

shortest_route,shortestDistance = UCS.UCSOSMNX.searchPath(orig_node, dest_node, graph)
print(shortest_route,shortestDistance)

# shortest_route_map,ax = ox.plot_graph_route(graph, shortest_route)
# plt.show(shortest_route_map)

#  find the shortest path
shortest_route = nx.shortest_path(graph,
                                  orig_node,
                                  dest_node,
                                  weight=optimizer)
shortestDistance = nx.shortest_path_length(graph,orig_node,dest_node,weight=optimizer)

print(shortest_route,shortestDistance)

shortest_route_map,ax = ox.plot_graph_route(graph, shortest_route)
plt.show(shortest_route_map)