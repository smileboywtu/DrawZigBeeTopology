# show the topology use graphviz
# python 3.4

import base64
import threading
import tkinter as tk
from graphviz import Digraph

updates_queue = Queue()

def init_graph():
    "init the graph and image panel"
    dot = Digraph()
    dot.name = "topology"
    dot.format = "gif"
    dot.comment = "topology tree of the zigbee network"
    dot.filename = "zigbee_topology"
    global graph_instance
    graph_instance = dot

def update_image_label(image_label):
    "use the timer to update the label image"
    global updates_queue
    while not updates_queue.empty():
        new_image = updates_queue.get()
        image_label.configure(image=new_image)
        image_label = new_image
        updates_queue.task_done()

def init_window():
    "init a window"
    root = tk.Tk()
    root.title("ZigBee Network Topology")
    text_lable = tk.Label(root, text="""
        this is the zigbee network topology,
        and now the network is running...""").pack(side="left")
    image_lable = tk.Label(root).pack(side="right")
    # use a timer to update the label
    root.after(100, update_image_label, (image_lable,))
    root.mainloop()

def init_window_graph():
    "init all"
    init_graph()
    init_window()

def add_new_edge(a, b):
    "add new edge to the graph"
    global graph_instance
    if None == graph_instance:
        init_window_graph()

    if a == b:
        graph_instance.node(a, "Coord")
    else:
        graph_instance.edge(a, b)

    # update
    global updates_queue
    raw_asc_image = graph_instance.pipe(format="gif")
    updates_queue.put(tk.PhotoImage(base64.b64encode(raw_asc_image)))
