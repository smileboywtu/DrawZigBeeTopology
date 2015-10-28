# show the topology use graphviz
# python 3.4

import base64
import threading
import tkinter as tk
from graphviz import Digraph

share_queue = Queue()

def init_graph():
    "init the graph and image panel"
    dot = Digraph()
    dot.name = "topology"
    dot.format = "gif"
    dot.filename = "zigbee_topology"
    global graph_handler
    graph_handler = dot

def update_image_label(label):
    "use the timer to update the label image"
    global share_queue
    while not share_queue.empty():
        image = share_queue.get()
        label.configure(image=image)
        label.image = image
        share_queue.task_done()

def init_view():
    "init a window"
    root = tk.Tk()
    root.title("ZigBee Network Topology")
    text_lable = tk.Label(root, text="""
            zigbee network topology
        and now the network is running,
        new added node will update the
        topology image.""")
    image_lable = tk.Label(root)
    text_lable.pack(side="left")
    image_lable.pack(side="right")

    root.after(100, update_image_label, (image_lable,))
    root.mainloop()

def init_all():
    "init all"
    init_graph()
    init_view()

def add_new_edge(a, b):
    "add new edge to the graph"
    global graph_handler
    if None == graph_handler:
        init_all()

    if a == b:
        graph_handler.node(a, "Coord")
    else:
        graph_handler.edge(a, b)

    global share_queue
    raw_asc_image = graph_handler.pipe(format="gif")
    share_queue.put(tk.PhotoImage(base64.b64encode(raw_asc_image)))