from firewall.firewall_commands import FirewallCommands
import thread
import utils

class Firewall(thread.Thread):

    def __init__(self, state):
        super().__init__('Firewall', state)
        self.commands = FirewallCommands()

    def _monitor(self):
        utils.safe_run(self._firewall_thread())

    def _firewall_thread(self):
        self.commands.set_standard_rules()
        while True:
            task = self.queue.get()
            if 'cmd' in task:
                payload = task['payload'] if 'payload' in task else None
                self.commands.get(task['cmd'])(payload)
            with self._lock:
                if not self._active:
                    break
