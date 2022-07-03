from functools import total_ordering
from re import I
import utils
import threading
import time
import queue
import socket
from state import State
import asyncio
import numpy as np

from tracker.tcp_dump_tracker import TcpDumpTracker
MSG_LEN = [10*1024*1024] #10*1024*1024, 100*1024*1024, 1000*1024*1024
NR_OF_MSG = 10
RECEIVE_IP = "192.168.2.1"
MAX_READ_LENGTH = 100*1024*1024
NR_OF_PORTS = 3
START_PORT = 8100
PORTS = [(START_PORT + i) for i in range(NR_OF_PORTS)]
total_received = {}
for port in PORTS:
    total_received[port] = [NR_OF_MSG * [0] for x in range(len(MSG_LEN))]
total_by_wetransfer = 0
current_iteration = 0
current_index = 0


def receive_packet(sock, length):
    """Receives a packet with specific size from 1 open socket

    Args:
        sock (Socket): An connected socket with 1 client
        length (int): Number of bytes that need to be received.

    Returns:
        int: The total anount of data received
    """
    remaining = length
    new_data = None
    while remaining:
        new_data = sock.recv(remaining if remaining<MAX_READ_LENGTH else MAX_READ_LENGTH)
        remaining -= len(new_data)
    return length
def receive_packets(sockets, length):
    """Receive a specific size of packets from the multiple open packets.

    Args:
        sockets (Socket[]): A list of open sockets
        length (int): The total size of the message that needs to be received.

    Returns:
        _type_: _description_
    """
    remaining = {}
    for port in sockets:
        remaining[port] = length
    new_data = None
    while sum(remaining.values()) > 0:
        for port in sockets:
            sock = sockets[port]
            new_data = sock.recv(remaining[port] if remaining[port]<MAX_READ_LENGTH else MAX_READ_LENGTH)
            remaining[port] -= len(new_data)
    return length

def clear_buffer(sock):
    """Clears buffer before listening to incoming new messages

    Args:
        sock (Socket): the socket connection with a speficic client
    """
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
    """Handles incoming packet and discards it if it is not from the sending source. 

    Args:
        packet (dict): The packet received by the sender including a random content.
    """
    global total_received, current_iteration, current_index,total_by_wetransfer
    if packet['dst'] == '52.218.56.176':
        total_by_wetransfer += packet['size']
    if packet['service'].isnumeric() and int(packet['service']) in PORTS:
        total_received[int(packet['service'])][current_index][current_iteration] += packet['size']


def _start_tracking():
    state = State()
    handler = TcpDumpTracker(state)
    asyncio.run(handler.start(handle_packet)) #, 'port 8100 or port 8101 or port 8102 or port 8103'


def start():
    """A benchmark for percentage of total packets captured by tcp_dump. It waits until specified packet is received by the multiple ports"""
    global current_iteration, current_index, total_received
    thread = threading.Thread(target=_start_tracking)
    print("Starting thread")
    thread.daemon = True
    thread.start()

    print('Setting up socket')
    rs = {}
    for port in PORTS:
        rs[port] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        rs[port].bind((RECEIVE_IP, port))
        rs[port].listen(1)
    
    newsocket = {}
    # I have accepted the TCP connection
    for port in PORTS:
        newsocket[port], addr = rs[port].accept()
        clear_buffer(newsocket[port])
        
    durations = [NR_OF_MSG * [0] for x in range(len(MSG_LEN))]
  
    for index, msg_size in enumerate(MSG_LEN):
        current_index = index
        for i in range(NR_OF_MSG):
            current_iteration = i
            print("Iteration: {}".format(current_iteration))
            tic = time.time()
            receive_packets(newsocket, msg_size)
            toc = time.time()
            durations[index][current_iteration] = toc-tic
            time.sleep(2)
    time.sleep(5)
    print("TOTAL RECEIVED By Dump")
    print(total_received)
    print("TOTAL RECEIVED By socket")
    print(MSG_LEN)
    print("Duration")
    print(durations)
    print(total_by_wetransfer)


if __name__ == '__main__':
    start()
