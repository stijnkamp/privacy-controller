import configparser
import sqlite3
import socket, fcntl, struct
CONFIG_PATH = "/etc/pihole/pihole-FTL.conf"
DHCP_PATH="/etc/pihole/dhcp.leases"
def getPiHoleConf():
    config = configparser.ConfigParser()
    with open(CONFIG_PATH, 'r') as f:
        config_string = '[DEFAULT]\n' + f.read()
    config.read_string(config_string)
    return config

def get_database_file():
    config = getPiHoleConf()
    if('DBFILE' in config): 
        return config['DBFILE']
    else:
        return "/etc/pihole/pihole-FTL.db"
def get_own_hwaddr():
    ifname = 'eth1'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', bytes(ifname, 'utf-8')[:15]))
    return ':'.join('%02x' % b for b in info[18:24])
def get_dhcp_leases():
    leases_addr = {}
    leases_ip = {}

    with open(DHCP_PATH, 'r') as f:
        dhcp_leases = f.readlines()
    for lease_line in dhcp_leases:
        lease_params = lease_line.split(" ")
        if len(lease_params) == 5:
            # time = int(lease_params[0])
            address = lease_params[1]
            ip = lease_params[2]
            leases_addr[ip] = address
            leases_ip[address] = ip

    return leases_ip, leases_addr