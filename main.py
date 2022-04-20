import utils
import threading
import time
from pihole import PiHole
from web_server import WebServer
from tracker import Tracker
from websocket import Websocket
def start():
    """Initialize the privacy controller start the multiple services
    - DNS/DHCP controller: pihole
    - Firewall controller: firewall
    """
    utils.log('[MAIN] Starting.')
    state = {}


    websocket_thread = Websocket(state)
    websocket_thread.start()

    pihole_thread = PiHole(state)
    pihole_thread.start()

    web_thread = WebServer(state)
    web_thread.start()

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
            print('')
            break
    

if __name__ == '__main__':
    start()
