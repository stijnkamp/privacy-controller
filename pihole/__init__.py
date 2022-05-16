import threading
import utils
import time
from watchdog.observers import Observer
from pihole.helpers import get_dhcp_leases
from pihole import dns_lookup, pihole_commands


class PiHole(object):
    def __init__(self, state):
        self._lock = threading.Lock()
        self._active = False

        self._thread = threading.Thread(target=self._pi_hole_monitor)
        self._thread.daemon = True
        self.state = state
        self.queue = state.get_queue('pihole')
        self.commands = pihole_commands.PiholeCommands()

    def start(self):

        with self._lock:
            self._active = True
        utils.log('[Pi Hole] Starting.')
        self._thread.start()

    def _pi_hole_monitor(self):

        utils.safe_run(self._pi_hole_thread)

    def get_dhcp_leases(self):
        dhcp_leases_ip, dhcp_leases_addr = get_dhcp_leases()

        self.state.dhcp_leases_ip.update(dhcp_leases_ip)
        self.state.dhcp_leases_addr.update(dhcp_leases_addr)

    def _pi_hole_thread(self):
        self.get_dhcp_leases()
        observer = Observer()
        path = '/etc/pihole/dhcp.leases'
        observer.schedule(self.get_dhcp_leases, path)
        while True:
            task = self.queue.get()
            if('cmd' in task):
                payload = task['payload'] if 'payload' in task else None
                self.commands.get(task['cmd'])(payload)
            with self._lock:
                if not self._active:
                    return

    def stop(self):
        with self._lock:
            self._active = False

        self._thread.join()

        utils.log('[Pi Hole] Stopped.')
