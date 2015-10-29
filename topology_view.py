 show the topology use graphviz
# python 3.4

import base64
import threading
import tkinter as tk
from datetime import time
from graphviz import Digraph

share_queue = Queue()

def update_label(root, label):
    "use the timer to update the label image"
    if not share_queue.empty():
        image = share_queue.get()
        label.configure(image=image)
        label.image = image
        share_queue.task_done()
        print(time.hour(), ":", time.minute(), ":", time.second(), " update the topology.")
    root.after(200, update_label, root, label)

def init_graph():
    "init the graph and image panel"
    dot = Digraph()
    dot.name = "topology"
    dot.format = "gif"
    dot.filename = "zigbee_topology"
    return dot

def start_view():
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

    root.after(200, update_label, root, image_lable)
    root.mainloop()

def add_new_edge(dot, a, b):
    "add new edge to the graph"
    if a == b:
        dot.node(a, "Coord")
    else:
        dot.edge(a, b)

    # add new image content
    asc_image = dot.pipe(format="gif")
    share_queue.put(tk.PhotoImage(base64.b64encode(asc_image)))
