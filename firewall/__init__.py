import threading
from firewall.firewall_commands import FirewallCommands
import utils
import logging
import time
import asyncio
import json
import secrets
import nftables
import os
import firewall.rule_parser


class Firewall(object):

    def __init__(self, state):
        self._lock = threading.Lock()
        self._active = False

        self._thread = threading.Thread(target=self._firewall_monitor)
        self._thread.daemon = True
        self.state = state
        self.queue = state.get_queue('firewall')
        self.commands = FirewallCommands()

    def start(self):
        with self._lock:
            self._active = True
        utils.log('[Firewall] Starting.')
        self._thread.start()

    def _firewall_monitor(self):
        utils.restart_upon_crash(self._firewall_thread())

    def running(self):
        with self._lock:
            return self._active
    def _firewall_thread(self):
        self.commands.set_standard_rules()
        while self.running():
            if not self.queue.empty():
                task = self.queue.get()
                if('cmd' in task):
                    payload = task['payload'] if 'payload' in task else None
                    self.commands.get(task['cmd'])(payload)
            else: 
                time.sleep(1)

    def stop(self):
        with self._lock:
            self._active = False
        self._thread.join()
        utils.log('[Firewall] Stopped.')
