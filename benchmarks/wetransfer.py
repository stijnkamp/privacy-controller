import threading
import time
from state import State
import asyncio

from tracker.tcp_dump_tracker import TcpDumpTracker

WETRANSFER_IP = "52.218.0.0/16"

total_received = 0

def handle_packet(packet):
    """Check if packet has been send from a specific location and port.

    Args:
        packet (dict): the packet received by TcpDumpTracker
    """
    global total_received
    if('52.218' in packet['dst']):
        total_received += packet['size']
        

def _start_tracking():
    global WETRANSFER_IP
    state = State()
    handler = TcpDumpTracker(state)
    asyncio.run(handler.start(handle_packet)) #, 'port 8100 or port 8101 or port 8102 or port 8103' , "dst net {}".format(WETRANSFER_IP)


def start():
    """A benchmark of percentage of total document sent by Wetransfer and captured by tcp_dump"""
    global total_received
    thread = threading.Thread(target=_start_tracking)
    print("Starting thread")
    thread.daemon = True
    thread.start()

    try:
        print('Press Ctrl+C to exit')
        while(True):
            time.sleep(1)
    except KeyboardInterrupt:
        print('got Ctrl+C')

    print(total_received)

if __name__ == '__main__':
    start()
