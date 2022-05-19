import thread
import utils
import logging
import time
import asyncio
import json
import secrets
import websockets
import config


class Websocket(thread.Thread):
    """
    Service to start a websocket which can send updated to the front-end in real-time.
    Clients can register to specific channels and it will get updates for those messages through a websocket.
    """

    def __init__(self, state):
        super().__init__('Websocket', state)
        # Keep track of all connected clients
        self.clients = []

    def _monitor(self):
        self.event_loop = asyncio.new_event_loop()
        utils.safe_run(self._websocket_thread())

    async def notify_clients(self):
        """Watch the queue and send message from queue to registered clients
        """
        while True:
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
        """Handle a connection and dispatch it according to who is connecting.

        Args:
            websocket (WebsocketClient): The websocket client that just connected.
            path (str): The path to which the client subscribed
        """

        client = {
            'websocket': websocket,
            'events': set()
        }
        self.clients.append(client)
        utils.log('New client registered')
        try:
            while True:
                message = await websocket.recv()
                if utils.is_json(message):
                    cmd = json.loads(message)
                    if('register' in cmd):
                        client['events'].add(cmd['register'])
                    if('unregister' in cmd):
                        client['events'].remove(cmd['unregister'])
        finally:
            self.clients.remove(client)

    async def check_for_stop(self):
        """Keep running until thread is not active
        """
        while self.running():
            await asyncio.sleep(1)
        self.event_loop.stop()

    def _websocket_thread(self):
        start_server = websockets.serve(self.handler, config.websocket['HOST'], config.websocket['PORT'], loop=self.event_loop)
        notify_clients = self.notify_clients()
        check_stop = self.check_for_stop()
        tasks = asyncio.wait([start_server, notify_clients, check_stop])
        try:
            self.event_loop.run_until_complete(tasks)
        except asyncio.CancelledError:
            self.event_loop.close()
