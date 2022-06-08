from firewall.firewall_commands import FirewallCommands
import thread
import utils

class Firewall(thread.Thread):
    """Setup the Firewall thread

    Args:
        state (State): The shared state with other services
    """
    def __init__(self, state):
        super().__init__('Firewall', state)
        self.commands = FirewallCommands()

    def _monitor(self):
        utils.safe_run(self.firewall_thread())

    def firewall_thread(self):
        """Set up the starting firewall rules and wait for a task in the queue to be executed.
        """
        self.commands.set_standard_rules()
        while True:
            task = self.queue.get()
            if 'cmd' in task:
                payload = task['payload'] if 'payload' in task else None
                if payload == None:
                    self.commands.get(task['cmd'])()
                else: 
                    self.commands.get(task['cmd'])(payload)
            with self._lock:
                if not self._active:
                    break
