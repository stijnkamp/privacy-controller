import subprocess, time, re, asyncio
import utils
import datetime

from web import db
from web.api.models import Traffic
def re_param(name, pattern):
    return f'(?P<{name}>{pattern})'

#Used from https://github.com/zaneclaes/network-traffic-metrics
pattern = '.*' + '.*'.join([
    'proto ' + re_param('proto', '\w+') + ' ',
    'length ' + re_param('length', '\d+'),
    '\n\s*' + re_param('src', '[\w\d\.-]+') + '\.' + re_param('srcp', '[\w\d-]+') +
    ' > ' +
    re_param('dst', '[\w\d\.-]+') + '\.' + re_param('dstp', '[\w\d-]+'),
]) + '.*'
tcpdump_matcher = re.compile(pattern)
service_matcher = re.compile('(?P<service>\w+)\s*(?P<port>\d+)/(?P<proto>\w+)')
class TcpDumpTracker(object):
    service_map = {}
    all_services = set()
    def __init__(self, state):
        with open('/etc/services') as f:
            for line in f.readlines():
                match = service_matcher.match(line)
                if not match: continue
                port = int(match.group('port'))
                if not port in self.service_map: self.service_map[port] = {}
                self.service_map[port][match.group('proto')] = match.group('service')
                self.all_services.add(match.group('service'))
    def get_service(self, port, proto):
        if not port in self.service_map: return None
        if not proto in self.service_map[port]: return None
        return self.service_map[port][proto]
    # Helper for building regex.
    
    def parse_packet(self, line):
        m = tcpdump_matcher.match(line)
        if not m:
            print('[SKIP] ' + line.replace("\n", "\t"))
            return

        labels = {
            'src': m.group('src'),
            'dst': m.group('dst'),
            'proto': m.group('proto').lower(),
            'service': None,
            'size': int(m.group('length')),
            'date_created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        # If the last part of the src/dst is a service, just use the literal service name:
        if m.group('dstp') in self.all_services: 
            labels['service'] = m.group('dstp')

        elif m.group('srcp') in self.all_services: labels['service'] = m.group('srcp')
        # Otherwise, do a lookup of port/proto to the service:
        if not labels['service'] and m.group('dstp').isnumeric():
            labels['service'] = self.get_service(m.group('dstp'), labels['proto'])
        if not labels['service'] and m.group('srcp').isnumeric():
            labels['service'] = self.get_service(m.group('srcp'), labels['proto'])
        if not labels['service']:
            labels['service'] = ""
        return labels
        # new_traffic = Traffic(**labels)
        # db.session.add(new_traffic) 
        # db.session.commit()   
    def getPacketKey(self, packet):
        return "%s.%s.%s.%s" % (packet['src'], packet['dst'], packet['proto'], packet['service'])
    async def start(self, packet_handler):
        p = await asyncio.create_subprocess_exec(
        'tcpdump', '-i', 'eth1', '-v', '-l', #, 'src net 192.168.2.0/24 or dst net 192.168.2.0/24'
        stdout=asyncio.subprocess.PIPE)
        prevPacketTime = None
        packets = {}
        while True:
            # When tcpdump is run with -v, it outputs two lines per packet;
            # readuntil ensures that each "line" is actually a parse-able string of output.
            line = await p.stdout.readuntil(b' IP ')
            if len(line) <= 0:
                print(f'No output from tcpdump... waiting.')
                time.sleep(1)
                continue
            
                    
            try:
                packet = self.parse_packet(line.decode('utf-8'))
                #only commit every second to decrease load on sql server
                if packet: 
                    packet_handler(packet)
                
            except BaseException as e:
                print(f'Failed to parse line "{line}" because: {e}')

