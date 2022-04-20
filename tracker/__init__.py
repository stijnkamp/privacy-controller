import subprocess, time, re, asyncio

import utils
import datetime
from tracker.tcp_dump_tracker import TcpDumpTracker
from tracker.scapy_tracker import ScapyTracker

from web import db
from web.api.models import Traffic

# Matchers

# Since we use a asyncio subprocess we do not need an extra thread.
class Tracker(object):
    def __init__(self, state):
        print(state)
        # self.handler = TcpDumpTracker(state)
        self.handler = ScapyTracker(state)
        self.packets = {}
        self.prevPacketTime = None
    def start(self):
        utils.log('[Tracker] Starting.')
        asyncio.run(self.handler.start(self.packet_handler))
    def getPacketKey(self, packet):
        return "%s.%s.%s.%s" % (packet['src'], packet['dst'], packet['proto'], packet['service'])
    def packet_handler(self, packet):
        if(self.getPacketKey(packet) not in self.packets):
            self.packets[self.getPacketKey(packet)] = packet
        else:
            self.packets[self.getPacketKey(packet)]['size'] += packet['size']
        if(packet['date_created'] != self.prevPacketTime):
            self.prevPacketTime = packet['date_created']
            for packet in self.packets.values():
                del packet['date_created']
                new_traffic = Traffic(**packet)
                db.session.add(new_traffic) 
            db.session.commit()   
            self.packets = {}
                    
    def stop(self):
        utils.log('[Tracker] Stopped.')