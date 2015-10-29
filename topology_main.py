# use python 3.4
# communicate with the coordinator

import time
import serial
import threading
from queue import Queue
from topology_view import start_view
from topology_view import init_graph
from topology_view import add_new_edge

relation_queue = Queue()

def read_run(ser_io):
    "read the data from the uart"
    while 1:
        relation = ser_io.read(4);
        self_address = hex(relation[1]) + hex(relation[0])[2:]
        parent_address = hex(relation[3]) + hex(relation[2])[2:]
        relation_queue.put((self_address, parent_address))
        time.sleep(.2)

def read_thread_def(uart):
    "read the topology information from the uart"
    read_thread = threading.Thread(target=read_run, args=(uart,))
    read_thread.daemon = True
    read_thread.start()

def draw_run():
    "handle the data from the queue"
    dot = init_graph()
    while 1:
        if not store.empty():
            self_address, parent_address = relation_queue.get()
            add_new_edge(dot, self_address, parent_address)
            relation_queue.task_done()
        time.sleep(1)

def draw_thread_def():
    "thread to draw the topology"
    draw_thread = threading.Thread(target=draw_run)
    draw_thread.daemon = True
    draw_thread.start()

def main():
    "this is the main frame work for this draw topology app"
    port_number = "COM3"
    with serial.Serial(
                        port=port_number,
                        baudrate=115200,
                        bytesize=serial.EIGHTBITS,
                        parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        timeout=None) as uart:
        read_thread_def(uart)
        draw_thread_def()

        print("main program is running...")
        start_view()
        print("program exit.")

if __name__ == '__main__':
    main()
