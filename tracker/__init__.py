import subprocess, time, re, asyncio
import threading
import utils
import datetime
from tracker.tcp_dump_tracker import TcpDumpTracker
from tracker.scapy_tracker import ScapyTracker

from web import db
from web.api.models import Traffic

from pihole.helpers import get_dhcp_leases
# Matchers

# Since we use a asyncio subprocess we do not need an extra thread.
class Tracker(object):
    def __init__(self, state):
        self._lock = threading.Lock()
        self._active = False

        self._thread = threading.Thread(target=self._tracker_monitor)
        self._thread.daemon = True

        self.handler = TcpDumpTracker(state)
        self.state = state
        self.packets = {}
        self.destinations = set()
        self.prevPacketTime = None
    def start(self):
        with self._lock:
            self._active = True
        utils.log('[Tracker] Starting.')
        self._thread.start()
        
    def _tracker_monitor(self):
        utils.restart_upon_crash(asyncio.run(self.handler.start(self.packet_handler)))
    def getPacketKey(self, packet):
        return "%s.%s.%s.%s" % (packet['src_ip'], packet['dst'], packet['proto'], packet['service'])
    def packet_handler(self, packet):
        if(self.getPacketKey(packet) not in self.packets):
            self.packets[self.getPacketKey(packet)] = packet
        else:
            self.packets[self.getPacketKey(packet)]['size'] += packet['size']
        self.destinations.add(packet['dst'])
        if(packet['date_created'] != self.prevPacketTime):
            self.prevPacketTime = packet['date_created']
            for packet in self.packets.values():
                if packet['src'] == None:
                    packet['src'] = self.state.dhcp_leases_addr[packet['src_ip']] if packet['src_ip'] in self.state.dhcp_leases_addr else packet['src_ip']
                del packet['date_created']
                del packet['src_ip']
                new_traffic = Traffic(**packet)
                db.session.add(new_traffic) 
            with self._lock:
                db.session.commit()
            self.state.send_command('pihole', {
                'cmd': 'resolve_destinations',
                'payload': self.destinations.copy()
            })
            self.destinations.clear()
            self.packets = {}
                    
    def stop(self):
        utils.log('[Tracker] Stopped.')