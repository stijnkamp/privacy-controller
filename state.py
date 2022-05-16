import queue
from pihole.helpers import get_own_hwaddr

class State(object):
    def __init__(self):
        self.workers = {
            'websocket': queue.SimpleQueue(),
            'firewall': queue.SimpleQueue(),
            'pihole': queue.SimpleQueue()
        }
        self.dhcp_leases_addr = {
            "192.168.2.1": get_own_hwaddr()
        }
        self.dhcp_leases_ip = {
            get_own_hwaddr(): "192.168.2.1"
        }
    
    def get_queue(self, worker):
        if(worker in self.workers):
            return self.workers[worker]
        return None
    def send_command(self, worker, cmd):
        if(worker in self.workers):
            self.workers[worker].put(cmd)