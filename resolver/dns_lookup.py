import utils
import re
import socket
import whois
import requests
LOG_PATH = "/var/log/pihole.log"


def reverse_dns(ip):
    """Get domain using reverse dns lookup using the socket package

    Args:
        ip (str): IPv4 address to find a domain for

    Returns:
        str: First domain that is connected to the IP address
    """
    domain = socket.getnameinfo((ip, 0), 0)
    return domain[0]


def get_domain_for_ip(ip):
    """Get domain of ip by first looking at the pihole logs to resolve a domain. If not found the ip address if found using the socket library. 

    Args:
        ip (str): IPv4 address to find a domain for

    Returns:
        str: First domain that is connected to the IP address
    """
    regex = "reply .+is {}".format(re.escape(ip))
    line = utils.search_in_file(LOG_PATH, regex)
    if line:
        domain = line.replace("reply ", "").replace(" is {}".format(ip), "")
    else:
        domain = reverse_dns(ip)
    return domain



def get_location_for_ip(ip):
    """Retrieve location of a specific IPv4 address using ip-api.com

    Args:
        ip (str): IPv4 address to find a domain for

    Returns:
        dict: The location including city, region, country and coordinates.
    """
    url = "https://ip-api.com/json/{}".format(ip)
    r = requests.get(url)
    data = r.json()
    if data['country'] == 'Not found':
        return False
    return {
        'city': data['city'],
        'region': data['regionName'],
        'country': data['country'],
        'lat': data['lat'],
        'lon': data['lon']
    }

def batch_location_for_ip(addresses):
    """Retrieve batch of locations for multiple IPv4 addresses at once using the ipinfo.io. Caution: this service stores your requests for other purposes.

    Args:
        addresses (str[]): A list of IPv4 addresses

    Returns:
        dict[]: A list of the found locations.
    """
    url = "https://ipinfo.io/batch"
    r = requests.post(url, json=list(addresses))
    data = r.json()
    return data

def get_company_for_domain(domain):
    """Find the organization that registered the domain using Whois. It first removes all subdomains from the domain.

    Args:
        domain (str): A registered domain

    Returns:
        str: Company name if present, otherwise None
    """
    domain = re.sub("^[^.]*\.(?=\w+\.\w+$)", "", domain)
    try:
        info = whois.whois(domain)
        company = info['org']
        if isinstance(company, list):
            return company[0]
        return company
    except Exception as e:
        return None

        
