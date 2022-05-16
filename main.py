import utils
import threading
import time
import queue
from pihole import PiHole
from web import WebServer
from tracker import Tracker
from websocket import Websocket
from firewall import Firewall
from state import State


def start():
    """Initialize the privacy controller start the multiple services
    - DNS/DHCP controller: pihole
    - Firewall controller: firewall
    """
    utils.log('[MAIN] Starting.')

    state = State()

    web_thread = WebServer(state)
    web_thread.start()

    websocket_thread = Websocket(state)
    websocket_thread.start()

    firewall_thread = Firewall(state)
    firewall_thread.start()

    pihole_thread = PiHole(state)
    pihole_thread.start()

    tracker_thread = Tracker(state)
    tracker_thread.start()

    quit = False
    while True:
        with threading.Lock():
            if quit:
                break
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            break
    utils.log("[MAIN] Closing application")
    web_thread.stop()
    websocket_thread.stop()
    firewall_thread.stop()
    pihole_thread.stop()
    tracker_thread.stop()


if __name__ == '__main__':
    start()
