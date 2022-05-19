import utils
import re
import socket
import whois
import requests
LOG_PATH = "/var/log/pihole.log"


def reverse_dns(ip):
    domain = socket.getnameinfo((ip, 0), 0)
    return domain[0]


def get_domain_for_ip(ip):
    regex = "reply .+is {}".format(re.escape(ip))
    line = utils.search_in_file(LOG_PATH, regex)
    if line:
        domain = line.replace("reply ", "").replace(" is {}".format(ip), "")
    else:
        domain = reverse_dns(ip)
    return domain


def get_location_for_ip(ip):
    url = "https://geolocation-db.com/json/{}".format(ip)
    r = requests.get(url)
    data = r.json()
    if data['country_code'] == 'Not found':
        return False
    return {
        'city': data['city'],
        'region': data['state'],
        'country': data['country_name'],
        'lat': data['latitude'],
        'lon': data['longitude']
    }


def get_company_for_domain(domain):
    domain = re.sub("^[^.]*\.(?=\w+\.\w+$)", "", domain)
    info = whois.whois(domain)
    return info['org']
