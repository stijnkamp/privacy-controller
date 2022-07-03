import thread
import utils
import watchdog.observers as observers
import resolver.helpers as resolver_helpers
import resolver.resolver_commands as commands


class Resolver(thread.Thread):
    """Resolver service which takes queue command to resolve ip addresses to more elaborate information.
    It also watches for new DHCP leases and updates the state with those DHCP leases. 

    Args:
        state (State): The shared state with other services
    """
    def __init__(self, state):
        super().__init__('Resolver', state)
        self.commands = commands.ResolverCommands()
        self.q = state.get_queue('Resolver')

    def _monitor(self):
        utils.safe_run(self._resolver_thread)

    def get_dhcp_leases(self):
        """Get the dhcp leases and store it in the state.
        """
        dhcp_leases_ip, dhcp_leases_addr = resolver_helpers.get_dhcp_leases()

        self.state.dhcp_leases_ip.update(dhcp_leases_ip)
        self.state.dhcp_leases_addr.update(dhcp_leases_addr)

    def _resolver_thread(self):
        self.get_dhcp_leases()
        observer = observers.Observer()
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
