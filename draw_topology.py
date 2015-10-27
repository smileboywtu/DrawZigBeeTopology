# use python 3.4
# communicate with the coordinator

import time
import serial
import threading
from queue import Queue
from graphviz_view import add_new_edge

store = Queue()

def read_run(ser_io):
    "read the data from the uart"
    while 1:
        relation = ser_io.read(4);
        # get self address
        self_address = hex(relation[1]) + hex(relation[0])[2:]
        # get parent address
        parent_address = hex(relation[3]) + hex(relation[2])[2:]
        # put in the queue
        store.put((self_address, parent_address))

def read_relation_thread(uart):
    "read the topology information from the uart"
    read_instance = threading.Thread(target=read_run, args=(uart,))
    read_instance.daemon = True
    read_instance.start()

def draw_run():
    "handle the data from the queue"
    while 1:
        if not store.empty():
            self_address, parent_address = store.get()
            # handle it
            add_new_edge(self_address, parent_address)
            # done this job
            store.task_done()

        time.sleep(1)

def draw_topology_thread():
    "thread to draw the topology"
    draw_instance = threading.Thread(target=draw_run)
    draw_instance.daemon = True
    draw_instance.start()

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
        read_relation_thread(uart)
        draw_topology_thread()
        while 1:
            print("main program is running...")
            is_exit = input("press esc to exit.")
            if 27 == ord(is_exit):
                print("uart closed.")
                break


if __name__ == '__main__':
    main()
