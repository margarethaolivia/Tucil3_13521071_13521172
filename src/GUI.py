import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import tkintermapview as tkMap
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import numpy as np
import networkx as nx
from pathlib import Path
import UCS
import Utils
import Map
import AStar

startCoord = None
endCoord = None
startMarker = None
endMarker = None
m = None
coord = None

root = ctk.CTk()  # create root window
root.title("PathFinder A* & UCS")  # title of the GUI window
root.geometry(f"{1100}x{700}")  # specify the max size the window can expand to

searchModeMap = IntVar()
searchModeGraph = IntVar()

startNodeGraph = StringVar()
endNodeGraph = StringVar()

def openFileGraph() :
    global m,coord
    file_path = askopenfile(mode='r', filetypes=[('text files', '*.txt')])
    if file_path is not None:
        fName = Path(file_path.name)
        filename.configure(text="File name : " + fName.name)
        searchGraphBtn.configure(state=NORMAL)
        m,coord = Utils.Util.readMatrix(file_path.name)
        plotGraph(m,coord)
        nodeList = []
        for i in range(len(m)) :
            nodeList.append(str(i))
        startCbBox.configure(values=nodeList)
        endCbBox.configure(values=nodeList)

def openFileMap() :
    map_path = askopenfile(mode='r', filetypes=[('text files', '*.xml'),('text files', '*.osm')])
    if (map_path is not None) :
        center = Map.MapPathSearch.saveGraphFile(map_path.name)
        map_widget.set_position(center[1],center[0])
        msgMapLbl.configure(text= "Map uploaded", text_color="white")
        msgMapLbl.place(relx=0.53,rely=0.72)

def searchGraph() :
    try :
        if(searchModeGraph.get() == 1) : # UCS
            shortest_route, shortest_dist = UCS.UCS.searchPath(int(startNodeGraph.get()),int(endNodeGraph.get()),m)
        elif (searchModeGraph.get() == 2) : # AStar
            shortest_route, shortest_dist = AStar.AStar.searchPath(int(startNodeGraph.get()),int(endNodeGraph.get()),m,coord)
        plotGraph(m,coord,shortest_route)
        dist_lbl_graph.configure(text="Shortest distance : " + str(shortest_dist) + " meter(s)")
        path = ""
        for i in range(len(shortest_route)) :
            if (i < len(shortest_route)-1) :
                path += str(shortest_route[i]) + " - "
            else :
                path += str(shortest_route[i])
        path_lbl_graph.configure(text="Path result : " + path, text_color="white")
    except :
        dist_lbl_graph.configure(text="Shortest distance : ")
        path_lbl_graph.configure(text="Path result : Path not found", text_color="red")

# Map functions
# def drawMarkers(coordList) :
#     # Menggambar marker berdasarkan list koordinat
#     count = 2
#     for coord in coordList :
#         map_widget.set_marker(coord[0], coord[1], text= "Node " +str(count))
#         count += 1

def add_start_coord(coords):
    # Menambahkan titik awal pada peta
    global startCoord, startMarker
    startCoord = (coords[1],coords[0])
    map_widget.delete_all_path()
    if (endCoord != None) :
        searchMapBtn.configure(state=NORMAL)
    if (startMarker != None) :
        startMarker.delete()
    # Menampilkan alamat pada koordinat yang ditunjuk
    addr = tkMap.convert_coordinates_to_address(coords[0],coords[1])
    displayAddr = ""
    if (addr.street != None) :
        displayAddr += addr.street
    if (addr.city != None and displayAddr != "") :
        displayAddr += ", " + addr.city
    startMarker = map_widget.set_marker(coords[0], coords[1], text=((displayAddr) if displayAddr != "" else "Start"))

def add_end_coord(coords):
    # Menambahkan titik akhir pada peta
    global endCoord, endMarker
    endCoord = (coords[1],coords[0])
    map_widget.delete_all_path()
    if (startCoord != None) :
        searchMapBtn.configure(state=NORMAL)
    if (endMarker != None) :
        endMarker.delete()
    # Menampilkan alamat pada koordinat yang ditunjuk
    addr = tkMap.convert_coordinates_to_address(coords[0],coords[1])
    displayAddr = ""
    if (addr.street != None) :
        displayAddr += addr.street
    if (addr.city != None and displayAddr != "") :
        displayAddr += ", " + addr.city
    endMarker = map_widget.set_marker(coords[0], coords[1], text=((displayAddr) if displayAddr != "" else "End"))

def search_path_map() :
    # Melakukan pencarian jalur pada peta
    map_widget.delete_all_path()
    msgMapLbl.place_forget()
    if (searchModeMap.get() == 1) :
        method = 'UCS'
    elif (searchModeMap.get() == 2) :
        method = 'A*'
    else :
        msgMapLbl.configure(text="Select a search method first !", text_color="red")
        msgMapLbl.place(relx=0.53,rely=0.72)
        return
    shortest_route, shortest_distance, graph, success = Map.MapPathSearch.search(startCoord,endCoord,method)
    if (success) :
        if (shortest_distance > 0) :
            shortest_route_coor = Map.MapPathSearch.convertPathToCoorPath(shortest_route,graph)
            map_widget.set_position(startCoord[1],startCoord[0])
            map_widget.set_zoom(15)
            dist_lbl.configure(text="Shortest distance : " + str(shortest_distance) + " meter(s)")
            map_widget.set_path(shortest_route_coor,color="red")
        else :
            dist_lbl.configure(text="Shortest distance : ")
            msgMapLbl.configure(text="Start and end is on the same node", text_color="red")
            msgMapLbl.place(relx=0.53,rely=0.72)
    else :
        dist_lbl.configure(text="Shortest distance : ")
        msgMapLbl.configure(text="Route not found", text_color="red")
        msgMapLbl.place(relx=0.53,rely=0.72)

def search_loc_map() :
    # Memindahkan posisi peta ke lokasi yang dicari
    msgMapLbl.place_forget()
    map_widget.delete_all_path()
    newCoord = tkMap.convert_address_to_coordinates(locTxtBox.get('0.0',END))
    if (newCoord != None) :
        map_widget.set_position(newCoord[0],newCoord[1])
        map_widget.set_zoom(15)
    else :
        msgMapLbl.configure(text="Location not found", text_color="red")
        msgMapLbl.place(relx=0.53,rely=0.72)

def plotGraph(m, coord, path=[]):
    # Menggambar graf di tempat yang disediakan
    adj_matrix = np.array(m)

    # Create a directed weighted graph from the weighted directed adjacency matrix
    graph = nx.Graph(adj_matrix)

    # Plot the directed weighted graph
    pos = {i: tuple(coord[i]) for i in range(len(coord))}

    # Draw graph with fixed node positions and edge labels
    a = fig.add_subplot(111)
    path_edges = []
    if (len(path) > 0) :
        for i in range(len(path)-1):
            path_edges.append(tuple((path[i], path[i+1])))
    nx.draw_networkx(graph, pos=pos, ax=a, with_labels=True, node_color=['blue' if e in path else 'lightblue' for e in graph.nodes()], 
                     node_size=500, font_size=14, font_weight='bold', edge_color=['red' if e in path_edges else 'black' for e in graph.edges()])
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={(
        i, j): f'{adj_matrix[i, j]:.1f}' for i, j in graph.edges()}, font_size=12, font_color='red', rotate=False)
    # edge_labels = nx.get_edge_attributes(self.graph, "weight")
    # nx.draw_networkx_edge_labels(self.graph, pos, edge_labels, rotate=False)
    plt.axis("off")
    canvas.draw()

# Title label
title = ctk.CTkLabel(root,text="A* and UCS Pathfinder",font=('Arial',25))
title.place(relx=0.37,rely=0.05)

# Graph display
graphFrame = ctk.CTkFrame(root, width=600, height=350, bg_color="transparent")
graphFrame.place(relx=0.05,rely=0.15)
fig = plt.Figure(figsize=(6, 3.58), dpi=100)
canvas = FigureCanvasTkAgg(fig, graphFrame)
toolbar = NavigationToolbar2Tk(canvas,graphFrame,pack_toolbar=False)
toolbar.update()
toolbar.pack(side=tk.BOTTOM, fill=tk.X)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Upload graph file button and labels
filename = ctk.CTkLabel(root,text="File name :")
filename.place(relx=0.1,rely=0.62)
dist_lbl_graph = ctk.CTkLabel(root,text="Shortest distance :")
dist_lbl_graph.place(relx=0.1,rely=0.65)
path_lbl_graph = ctk.CTkLabel(root,text="Path :")
path_lbl_graph.place(relx=0.1,rely=0.68)
uploadGraphBtn = ctk.CTkButton(root,text="Upload Graph",command=openFileGraph)
uploadGraphBtn.place(relx=0.16,rely=0.73)

# Graph start node and end node select
startCbBox = ctk.CTkComboBox(root, values=[''], variable=startNodeGraph, width=100)
startCbBox.set("Start Node")
startCbBox.place(relx=0.12,rely=0.78)
endCbBox = ctk.CTkComboBox(root, values=[''], variable=endNodeGraph, width=100)
endCbBox.set("End Node")
endCbBox.place(relx=0.24,rely=0.78)

# Search graph button
searchGraphBtn = ctk.CTkButton(root,text="Search",command=searchGraph,state="disabled")
searchGraphBtn.place(relx=0.16,rely=0.83)

# Search mode select button graph
UCSGraphBtn = ctk.CTkRadioButton(root,text="UCS", variable=searchModeGraph, value=1)
UCSGraphBtn.place(relx=0.18,rely=0.88)
AStarMapBtn = ctk.CTkRadioButton(root,text="A*", variable=searchModeGraph, value=2)
AStarMapBtn.place(relx=0.18,rely=0.92)

# Search location textbox and button
locTxtBox = ctk.CTkTextbox(root,width=300,height=30,activate_scrollbars=False)
locTxtBox.place(relx=0.63,rely=0.67)
searchLocBtn = ctk.CTkButton(root,text="Search Location",width=40,height=30,command=search_loc_map)
searchLocBtn.place(relx=0.53,rely=0.67)

# Error label
msgMapLbl = ctk.CTkLabel(root,height=10)

# Upload map button
uploadMapBtn = ctk.CTkButton(root, text="Upload Map", command=openFileMap)
uploadMapBtn.place(relx=0.65,rely=0.75)

# Search Map button
searchMapBtn = ctk.CTkButton(root,text="Search Path",command=search_path_map,state="disabled")
searchMapBtn.place(relx=0.65,rely=0.8)

# Search mode select button map
UCSMapBtn = ctk.CTkRadioButton(root,text="UCS", variable=searchModeMap, value=1)
UCSMapBtn.place(relx=0.665,rely=0.85)
AStarMapBtn = ctk.CTkRadioButton(root,text="A*", variable=searchModeMap, value=2)
AStarMapBtn.place(relx=0.665,rely=0.9)

# Map widget
map_widget = tkMap.TkinterMapView(root, width=600, height=400, corner_radius=0)
map_widget.place(relx=0.5,rely=0.15)
dist_lbl = ctk.CTkLabel(root,text="Shortest distance :")
dist_lbl.place(relx=0.53,rely=0.62)

map_widget.add_right_click_menu_command(label="Add start point",
                                        command=add_start_coord,
                                        pass_coords=True)
map_widget.add_right_click_menu_command(label="Add end point",
                                        command=add_end_coord,
                                        pass_coords=True)

root.mainloop()