# use python 3.4
# communicate with the coordinator

import time
import serial
import threading
from queue import Queue
from topology_view import add_new_edge
 
store = Queue()

def read_run(ser_io):
    "read the data from the uart"
    while 1:
        relation = ser_io.read(4);
        self_address = hex(relation[1]) + hex(relation[0])[2:]
        parent_address = hex(relation[3]) + hex(relation[2])[2:]
        store.put((self_address, parent_address))

def read_thread_def(uart):
    "read the topology information from the uart"
    read_thread = threading.Thread(target=read_run, args=(uart,))
    read_thread.daemon = True
    read_thread.start()

def draw_run():
    "handle the data from the queue"
    while 1:
        if not store.empty():
            self_address, parent_address = store.get()
            add_new_edge(self_address, parent_address)
            store.task_done()
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
        while 1:
            print("main program is running...")
            is_exit = input("press esc to exit.")
            if 27 == ord(is_exit):
                print("uart closed.")
                break

if __name__ == '__main__':
    main()