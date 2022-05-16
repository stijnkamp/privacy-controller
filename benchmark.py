import utils
import threading
import time
import queue
import socket
from state import State
import asyncio

from tracker.tcp_dump_tracker import TcpDumpTracker
MSG_LEN = 1024*1024
NR_OF_MSG = 10
RECEIVE_IP = "192.168.2.1"
PORT = 8111

total_received = NR_OF_MSG * [0]
current_iteration = 0
def receive_packet(sock, length):
    remaining = length
    data = bytearray()
    new_data = None
    while remaining:
        new_data = sock.recv(remaining)
        remaining -= len(new_data)
        data += new_data
    return data
def clear_buffer(sock):
    print("CLEARING BUFFER")
    sock.setblocking(0)
    try:
        while sock.recv(1024):
            pass
    except:
        pass
    sock.setblocking(1)
    print("DONE CLEARING BUFFER")
def handle_packet(packet):
    global total_received, current_iteration
    if packet['service'].isnumeric() and int(packet['service']) == PORT:
        print(current_iteration)
        total_received[current_iteration] += packet['size']
        print("RECEIVED")
def _start_tracking():
    state = State()
    handler = TcpDumpTracker(state)
    asyncio.run(handler.start(handle_packet, 'port 8111'))
def start():
    utils.log('[MAIN] Starting.')
    thread = threading.Thread(target=_start_tracking)
    print("Starting thread")
    thread.daemon = True
    thread.start()

    print('Setting up socket')
    rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    rs.bind((RECEIVE_IP, PORT))
    rs.listen(1) 

    # I have accepted the TCP connection
    newsocket, addr = rs.accept()
    clear_buffer(newsocket)
    total_by_socket = 0
    for i in range(NR_OF_MSG):
        current_iteration = i
        print("GOING TO INTERCEPT")
        print(current_iteration)
        data = receive_packet(newsocket, MSG_LEN)
        total_by_socket += len(data)
    time.sleep(5)
    print("TOTAL RECEIVED By Dump")
    print(total_received)
    print("TOTAL RECEIVED By socket")
    print(total_by_socket)
    print("PERCENTAGE")
    print(total_received*100/total_by_socket)

if __name__ == '__main__':
    start()
