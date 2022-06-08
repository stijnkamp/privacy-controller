import subprocess
import time
import re
import asyncio
from xml.dom.pulldom import START_ELEMENT
import utils
import datetime
import utils
from web import db
from web.api.models import Traffic


def re_param(name, pattern):
    return f'(?P<{name}>{pattern})'


# Used from https://github.com/zaneclaes/network-traffic-metrics
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
    def __init__(self, state):
        self.state = state
    # Helper for building regex.

    def parse_packet(self, line):
        m = tcpdump_matcher.match(line)
        if not m:
            utils.log('[SKIP] ' + line.replace("\n", "\t"))
            return
        if utils.is_ip4(m.group('src')) == False:
            utils.log('[SKIP] {} is not a ip address'.format(m.group('src')))
            return
        labels = {
            'src': None,
            'src_ip': m.group('src'),
            'dst': m.group('dst'),
            'proto': m.group('proto').lower(),
            'service': m.group('srcp') if m.group('dstp').isnumeric() else m.group('dstp'),
            'size': int(m.group('length')),
            'date_created': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        return labels
        # new_traffic = Traffic(**labels)
        # db.session.add(new_traffic)
        # db.session.commit()

    async def start(self, packet_handler, filter='src net 192.168.2.0/24 and not port ssh'):
        p = await asyncio.create_subprocess_exec(
            'tcpdump', '-i', 'eth1', '-v', '-n', '-l', filter,
            stdout=asyncio.subprocess.PIPE)
        prevPacketTime = None
        packets = {}
        while True:
            # When tcpdump is run with -v, it outputs two lines per packet;
            # readuntil ensures that each "line" is actually a parse-able string of output.
            line = await p.stdout.readuntil(b' IP ')
            if len(line) <= 0:
                utils.log(f'No output from tcpdump... waiting.')
                time.sleep(1)
                continue

            try:
                packet = self.parse_packet(line.decode('utf-8'))
                # only commit every second to decrease load on sql server
                if packet:
                    packet_handler(packet)

            except BaseException as e:
                utils.log(f'Failed to parse line "{line}" because: {e}')
