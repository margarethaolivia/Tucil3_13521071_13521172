import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import tkintermapview as tkMap
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pathlib import Path
import UCS
import Utils
import Map

startCoord = None
endCoord = None
startMarker = None
endMarker = None

root = ctk.CTk()  # create root window
root.title("PathFinder A* & UCS")  # title of the GUI window
root.geometry(f"{1100}x{700}")  # specify the max size the window can expand to

searchModeMap = IntVar()
searchModeGraph = IntVar()

def openFile() :
    global file_path
    file_path = askopenfile(mode='r', filetypes=[('text files', '*.txt')])
    if file_path is not None:
        fName = Path(file_path.name)
        filename.configure(text="File name : " + fName.name)
        searchGraphBtn.configure(state=NORMAL)

def searchGraph() :
    m = Utils.Graph.readMatrix(file_path.name)
    a = UCS.UCS(0,6,m)

# Map functions
def add_start_coord(coords):
    global startCoord, startMarker
    startCoord = coords
    map_widget.delete_all_path()
    if (endCoord != None) :
        searchMapBtn.configure(state=NORMAL)
    if (startMarker != None) :
        startMarker.delete()
    print("Add start point:", coords)
    startMarker = map_widget.set_marker(coords[0], coords[1], text="start")

def add_end_coord(coords):
    global endCoord, endMarker
    endCoord = coords
    map_widget.delete_all_path()
    if (startCoord != None) :
        searchMapBtn.configure(state=NORMAL)
    if (endMarker != None) :
        endMarker.delete()
    print("Add end point:", coords)
    endMarker = map_widget.set_marker(coords[0], coords[1], text="end")

def search_path_map(mode='walk') :
    map_widget.delete_all_path()
    errorMapLbl.place_forget()
    if (searchModeMap.get() == 1) : # UCS
        method = 'UCS'
    elif (searchModeMap.get() == 2) : # Built In
        method = 'BuiltIn'
    else :
        dist_lbl.configure(text="Select a serch method first !")
        return
    shortest_route, shortest_distance, graph, success = Map.MapPathSearch.search(startCoord,endCoord,mode,method)
    if (success) :
        shortest_route_coor = Map.MapPathSearch.convertPathToCoorPath(shortest_route,graph)
        map_widget.set_position(startCoord[0],startCoord[1])
        map_widget.set_zoom(15)
        dist_lbl.configure(text="Shortest distance : " + str(shortest_distance) + " meters")
        path = map_widget.set_path(shortest_route_coor,color="red")
    else :
        errorMapLbl.configure(text="Route not found", text_color="red")
        errorMapLbl.place(relx=0.53,rely=0.73)

def search_loc_map() :
    errorMapLbl.place_forget()
    map_widget.delete_all_path()
    newCoord = tkMap.convert_address_to_coordinates(locTxtBox.get('0.0',END))
    if (newCoord != None) :
        map_widget.set_position(newCoord[0],newCoord[1])
        map_widget.set_zoom(15)
    else :
        errorMapLbl.configure(text="Location not found", text_color="red")
        errorMapLbl.place(relx=0.53,rely=0.73)

# Title label
title = ctk.CTkLabel(root,text="A* and UCS Pathfinder",font=('Arial',25))
title.place(relx=0.37,rely=0.05)

# Graph display
figure1 = plt.Figure(figsize=(6, 4), dpi=100)
bar1 = FigureCanvasTkAgg(figure1, root)
bar1.get_tk_widget().place(relx=0.05,rely=0.15)

# Upload graph file button
filename = ctk.CTkLabel(root,text="File name :")
filename.place(relx=0.1,rely=0.62)
dist_lbl_graph = ctk.CTkLabel(root,text="Shortest distance :")
dist_lbl_graph.place(relx=0.1,rely=0.65)
uploadFileBtn = ctk.CTkButton(root,text="Upload",command=openFile)
uploadFileBtn.place(relx=0.16,rely=0.7)

# Search graph button
searchGraphBtn = ctk.CTkButton(root,text="Search",command=searchGraph,state="disabled")
searchGraphBtn.place(relx=0.16,rely=0.75)

# Search mode select button graph
UCSGraphBtn = ctk.CTkRadioButton(root,text="UCS", variable=searchModeGraph, value=1)
UCSGraphBtn.place(relx=0.18,rely=0.8)
AStarMapBtn = ctk.CTkRadioButton(root,text="A*", variable=searchModeGraph, value=2)
AStarMapBtn.place(relx=0.18,rely=0.85)

# Search location textbox and button
locTxtBox = ctk.CTkTextbox(root,width=300,height=30,activate_scrollbars=False)
locTxtBox.place(relx=0.63,rely=0.67)
searchLocBtn = ctk.CTkButton(root,text="Search Location",width=40,height=30,command=search_loc_map)
searchLocBtn.place(relx=0.53,rely=0.67)

# Error label
errorMapLbl = ctk.CTkLabel(root,height=10)

# Search Map button
searchMapBtn = ctk.CTkButton(root,text="Search Path",command=search_path_map,state="disabled")
searchMapBtn.place(relx=0.65,rely=0.75)

# Search mode select button map
UCSMapBtn = ctk.CTkRadioButton(root,text="UCS", variable=searchModeMap, value=1)
UCSMapBtn.place(relx=0.665,rely=0.8)
BuiltInMapBtn = ctk.CTkRadioButton(root,text="Built in", variable=searchModeMap, value=2)
BuiltInMapBtn.place(relx=0.665,rely=0.85)

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

# x = ['Col A', 'Col B', 'Col C']

# y = [50, 20, 80]

# fig = Figure(figsize=(4, 5))
# (x=x, height=y)

# # You can make your x axis labels vertical using the rotation
# plt.xticks(x, rotation=90)

# # specify the window as master
# canvas = FigureCanvasTkAgg(fig, master=display_frame)
# canvas.draw()
# canvas.get_tk_widget().grid(row=1, column=0, ipadx=40, ipady=20)

# # navigation toolbar
# toolbarFrame = Frame(master=display_frame)
# toolbarFrame.grid(row=2,column=0)
# toolbar = NavigationToolbar2Tk(canvas, toolbarFrame)
root.mainloop()
