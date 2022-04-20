import threading
import utils
import logging
import time
import asyncio
import json
import secrets
import websockets
class Websocket(object):

    def __init__(self, state):
        self._lock = threading.Lock()
        self._active = False

        self._thread = threading.Thread(target=self._websocket_monitor)
        self._thread.daemon = True

    def start(self):

        with self._lock:
            self._active = True
        utils.log('[Websocket] Starting.')
        self._thread.start()
    def _websocket_monitor(self):
        utils.restart_upon_crash(asyncio.run(self._websocket_thread()))
    

    async def handler(self, websocket, path):
        """
        Handle a connection and dispatch it according to who is connecting.

        """
        # Receive and parse the "init" event from the UI.
        message = await websocket.recv()
        print(message)
        
        print(path)
        
    async def _websocket_thread(self):
        async with websockets.serve(self.handler, "0.0.0.0", 8001):
            await asyncio.Future()  # run forever
    def stop(self):
        with self._lock:
            self._active = False
        self._thread.join()
        utils.log('[Websocket] Stopped.')