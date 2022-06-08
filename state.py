import multiprocessing 
from resolver.helpers import get_own_hwaddr


class State(object):
    def __init__(self):
        self.workers = {
            'Websocket': multiprocessing.Queue(),
            'Firewall': multiprocessing.Queue(),
            'Resolver': multiprocessing.Queue()
        }
        self.dhcp_leases_addr = {
            "192.168.2.1": get_own_hwaddr()
        }
        self.dhcp_leases_ip = {
            get_own_hwaddr(): "192.168.2.1"
        }
        self.user = None

    def get_queue(self, worker):
        """Retrieve queue if it exists for particular service

        Args:
            worker (str): Service name

        Returns:
            multiprocessing.Queue: The specific worker queue
        """
        if(worker in self.workers):
            return self.workers[worker]
        return None

    def send_command(self, worker, cmd):
        """Add command to a specific queue

        Args:
            worker (str): Service name
            cmd (dict): The command for a specific service worker.
        """
        if(worker in self.workers):
            self.workers[worker].put(cmd)
