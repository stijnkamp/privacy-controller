import subprocess
import time
import re
import asyncio
import utils
import datetime

from web import db
from web.api.models import Traffic
import scapy.all as sc


class ScapyTracker(object):
    def __init__(self, state):
        self._active = True
        self.packet_handler = None

    def get_packet_size(self, p):
        if sc.TCP in p:
            return len(p[sc.TCP].payload)
        elif sc.UDP in p:
            return len(p[sc.UDP].payload)
        elif sc.Raw in p:
            return len(p[sc.Raw].load)
        return 0

    def parse_packet(self, pkt):
        if sc.IP not in pkt:
            return
        packetSize = self.get_packet_size(pkt)
        if packetSize == 0:
            return
        packet = {
            'src': None,
            'src_ip': pkt[sc.IP].src,
            'dst': pkt[sc.IP].dst,
            'proto': pkt.sprintf("%IP.proto%"),
            'service': None,
            'size': packetSize,
            'date_created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        if sc.Ether in pkt:
            packet['src'] = pkt[sc.Ether].src
        if(sc.TCP in pkt):
            packet['service'] = pkt.sprintf("%TCP.sport%") if pkt.sprintf(
                "%TCP.dport%").isnumeric() else pkt.sprintf("%TCP.dport%")
        elif(sc.UDP in pkt):
            packet['service'] = pkt.sprintf("%UDP.sport%") if pkt.sprintf(
                "%UDP.dport%").isnumeric() else pkt.sprintf("%UDP.dport%")

        self.packet_handler(packet)

    async def start(self, packet_handler):
        self.packet_handler = packet_handler
        utils.safe_run(sc.sniff, kwargs={
            'iface': 'eth1',
            'prn': self.parse_packet,
            'stop_filter': lambda _: not self._active,
            'filter': 'src net 192.168.2.0/24 and not port ssh'
        })
