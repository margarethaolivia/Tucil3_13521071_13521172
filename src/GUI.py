import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import tkintermapview as tkMap
import matplotlib as plt
import UCS
import Utils
import Map
plt.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

startCoord = None
endCoord = None
startMarker = None
endMarker = None

root = Tk()  # create root window
root.title("PathFinder A* & UCS")  # title of the GUI window
root.geometry(f"{1400}x{700}")  # specify the max size the window can expand to
root.config(bg="skyblue")  # specify background color

searchModeMap = IntVar()

def openFile() :
    global file_path
    file_path = askopenfile(mode='r', filetypes=[('text files', '*.txt')])
    if file_path is not None:
        filename["text"] = file_path.name
        searchGraphBtn["state"] = "enabled"

def searchGraph() :
    m = Utils.Graph.readMatrix(file_path.name)
    a = UCS.UCS(0,6,m)

# Map functions
def add_start_coord(coords):
    global startCoord, startMarker
    startCoord = coords
    if (endCoord != None) :
        searchMapBtn["state"] = "enabled"
    if (startMarker != None) :
        startMarker.delete()
    print("Add start point:", coords)
    startMarker = map_widget.set_marker(coords[0], coords[1], text="start")

def add_end_coord(coords):
    global endCoord, endMarker
    endCoord = coords
    if (startCoord != None) :
        searchMapBtn["state"] = "enabled"
    if (endMarker != None) :
        endMarker.delete()
    print("Add end point:", coords)
    endMarker = map_widget.set_marker(coords[0], coords[1], text="end")

def search_map(mode='walk') :
    map_widget.delete_all_path()
    if (searchModeMap.get() == 1) : # UCS
        method = 'UCS'
    elif (searchModeMap.get() == 2) : # Built In
        method = 'BuiltIn'
    else :
        dist_lbl["text"] = "Select a serch method first !"
        return
    shortest_route, shortest_distance, graph = Map.MapPathSearch.search(startCoord,endCoord,mode,method)
    shortest_route_coor = Map.MapPathSearch.convertPathToCoorPath(shortest_route,graph)
    map_widget.set_position(startCoord[0],startCoord[1])
    map_widget.set_zoom(16)
    dist_lbl["text"] = "Shortest distance : " + str(shortest_distance) + " meters"
    path = map_widget.set_path(shortest_route_coor,color="red")

# Graph frame
graph_frame = Frame(root, width=650, height=700)
graph_frame.place(relx=0.25,rely=0.5,anchor=tk.CENTER)

# Map frame
map_frame = Frame(root, width=650, height=700)
map_frame.place(relx=0.75,rely=0.5,anchor=tk.CENTER)

# Upload file button
filename = Label(graph_frame,text="Upload graph file")
filename.place(relx=0.3,rely=0.7)
uploadFileBtn = Button(graph_frame,text="Upload",command=openFile)
uploadFileBtn.place(relx=0.3,rely=0.8)

# Search graph button
searchGraphBtn = Button(graph_frame,text="Search",command=searchGraph,state="disabled")
searchGraphBtn.place(relx=0.3,rely=0.9)

# Search Map button
searchMapBtn = Button(map_frame,text="Search Map",command=search_map,state="disabled")
searchMapBtn.place(relx=0.45,rely=0.7)

# Search mode select button map
UCSMapBtn = Radiobutton(map_frame,text="UCS", variable=searchModeMap, value=1)
UCSMapBtn.place(relx=0.45,rely=0.75)
BuiltInMapBtn = Radiobutton(map_frame,text="Built in", variable=searchModeMap, value=2)
BuiltInMapBtn.place(relx=0.45,rely=0.8)

# Map widget
map_widget = tkMap.TkinterMapView(map_frame, width=500, height=350, corner_radius=0)
map_widget.place(relx=0.1,rely=0.1)
dist_lbl = Label(map_frame,text="Shortest distance :")
dist_lbl.place(relx=0.4,rely=0.6)

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
