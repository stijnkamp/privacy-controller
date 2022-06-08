import utils
import time
from resolver.thread import Resolver
from web.web_server import WebServer
from tracker.thread import Tracker
from websocket.thread import Websocket
from firewall.thread import Firewall
from state import State
import startup


def start():
    """Initialize the privacy controller and start the multiple services"""
    utils.log('Starting.')
    startup.setup()
    
    # create the global state
    state = State()
    
    #Defining the different services
    thread_classes = [WebServer, Websocket, Firewall, Resolver, Tracker]
    threads = [thread(state) for thread in thread_classes]

    # Starting the threads
    for thread in threads:
        thread.start()

    #Keep main thread alive until keyboard interrupt
    while True:
        try:
            time.sleep(2)
        except KeyboardInterrupt:
            break
    #Terminate all threads
    utils.log("Closing")
    for thread in threads:
        thread.stop()

if __name__ == '__main__':
    start()
