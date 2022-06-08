import multiprocessing
import subprocess
import time
import re
import asyncio
import thread
import utils
import config
import datetime
from tracker.tcp_dump_tracker import TcpDumpTracker
from tracker.scapy_tracker import ScapyTracker

from web import db
from web.api.models import Traffic

from resolver.helpers import get_dhcp_leases
# Matchers

# Since we use a asyncio subprocess we do not need an extra thread.


class Tracker(thread.Thread):
    def __init__(self, state):
        super().__init__('Tracker', state)
        self.handler = TcpDumpTracker(state)
        self.packets = {}
        self.destinations = set()
        self.sources = set()
        self.prevPacketTime = None

    def _monitor(self):
        utils.safe_run(asyncio.run(
            self.handler.start(self.packet_handler)))

    def getPacketKey(self, packet):
        return {
            'src': packet["src_ip"],
            'dst': f'{packet["src_ip"]}.{packet["dst"]}',
            'proto': f'{packet["src_ip"]}.{packet["dst"]}.{packet["proto"]}',
            'service': f'{packet["src_ip"]}.{packet["dst"]}.{packet["proto"]}.{packet["service"]}'
        }[config.packet_granularity]

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
                    if packet['src_ip'] in self.state.dhcp_leases_addr:
                        packet['src'] = self.state.dhcp_leases_addr[packet['src_ip']]
                    else:
                        #If it is not in the dhcp list we will look it up within the resolver
                        packet['src'] = packet['src_ip']
                        self.sources.add(packet['src_ip'])
                del packet['date_created']
                del packet['src_ip']
                new_traffic = Traffic(**packet)
                db.session.add(new_traffic)
            with self._lock:
                db.session.commit()
            self.state.send_command('Resolver', {
                'cmd': 'resolve_destinations',
                'payload': self.destinations.copy()
            })
            if len(self.sources) > 0:
                self.state.send_command('Resolver', {
                    'cmd': 'resolve_sources',
                    'payload': self.sources.copy()
                })
                self.sources.clear()
            self.destinations.clear()
            self.packets = {}
