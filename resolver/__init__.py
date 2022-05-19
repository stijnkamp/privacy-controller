import thread
import utils
import time
from watchdog.observers import Observer
from resolver.helpers import get_dhcp_leases
from resolver import dns_lookup, resolver_commands


class Resolver(thread.Thread):
    def __init__(self, state):
        super().__init__('Resolver', state)
        self.commands = resolver_commands.ResolverCommands()
        self.q = state.get_queue('Resolver')

    def _monitor(self):
        utils.safe_run(self._resolver_thread)

    def get_dhcp_leases(self):
        dhcp_leases_ip, dhcp_leases_addr = get_dhcp_leases()

        self.state.dhcp_leases_ip.update(dhcp_leases_ip)
        self.state.dhcp_leases_addr.update(dhcp_leases_addr)

    def _resolver_thread(self):
        self.get_dhcp_leases()
        observer = Observer()
        path = '/etc/pihole/dhcp.leases'
        observer.schedule(self.get_dhcp_leases, path)
        while True:
            task = self.queue.get()
            if('cmd' in task):
                payload = task['payload'] if 'payload' in task else None
                cmd = self.commands.get(task['cmd'])
                if(cmd):
                    cmd(payload)
            with self._lock:
                if not self._active:
                    break
