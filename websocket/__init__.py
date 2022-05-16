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
        self.clients = []
        self.state = state
        self.queue = state.get_queue('websocket')

    def start(self):
        with self._lock:
            self._active = True
        utils.log('[Websocket] Starting.')
        self.event_loop = asyncio.new_event_loop()
        self._thread.start()

    def _websocket_monitor(self):
        utils.safe_run(self._websocket_thread())

    async def notify_clients(self):
        while self.running():
            notification = await self.event_loop.run_in_executor(None, self.queue.get)
            if('event' in notification):
                for client in self.clients:
                    if notification['event'] in client['events']:
                        if('payload' not in notification):
                            notification['payload'] = None
                        if isinstance(notification['payload'], object):
                            notification['payload'] = json.dumps(
                                notification['payload'])
                        await client['websocket'].send(notification['payload'])

    async def handler(self, websocket, path):
        """
        Handle a connection and dispatch it according to who is connecting.
        """
        # Register.
        client = {
            'websocket': websocket,
            'events': set()
        }
        self.clients.append(client)
        utils.log('Client refistered')
        try:
            while self.running():
                message = await websocket.recv()
                if utils.is_json(message):
                    cmd = json.loads(message)
                    if('register' in cmd):
                        client['events'].add(cmd['register'])
                    if('unregister' in cmd):
                        client['events'].remove(cmd['unregister'])
        finally:
            # Unregister.
            self.clients.remove(client)

    async def check_for_stop(self):
        while self.running():
            await asyncio.sleep(1)
        for task in asyncio.all_tasks():
            print(task)
            task.cancel()

    def running(self):
        with self._lock:
            return self._active

    async def start_server(self):
        start_server = websockets.serve(
            self.handler, "0.0.0.0", 8001, loop=self.event_loop)
        async with start_server:
            while(self.running()):
                await asyncio.sleep(1)

    def _websocket_thread(self):
        start_server = self.start_server
        notify_clients = self.notify_clients()
        check_stop = self.check_for_stop()
        print("CREATEING WAIT")
        cors = asyncio.wait([start_server, notify_clients, check_stop])
        try:
            self.event_loop.run_until_complete(cors)
        except asyncio.CancelledError:
            print("CLOSING")
            self.event_loop.close()

    def stop(self):
        utils.log("Stopping websocket")
        with self._lock:
            self._active = False
        self._thread.join()
        utils.log('[Websocket] Stopped.')
