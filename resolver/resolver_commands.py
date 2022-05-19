from web import db
from web.api import models as api_models
from web.pihole import models as pihole_models
from web.helpers import get_or_create
import threading
import utils
from resolver import dns_lookup


class ResolverCommands(object):
    def __init__(self):
        self._lock = threading.Lock()

    def resolve_destinations(self, destinations):
        with self._lock:
            known_destinations = db.session.query(api_models.Server.ip).filter(
                api_models.Server.ip.in_(destinations)).all()
        known_destinations = set(
            map(lambda known: known.ip, known_destinations))
        new_destinations = destinations.difference(set(known_destinations))
        for destination in new_destinations:
            if "192.168.2." in destination:
                continue
            domain = dns_lookup.get_domain_for_ip(destination)
            location = dns_lookup.get_location_for_ip(destination)
            company = dns_lookup.get_company_for_domain(domain)
            with self._lock:
                server_data = {
                    'ip': destination
                }

                if company != None:
                    server_data['company'] = get_or_create(
                        db.session, api_models.Company, name=company)
                if location != False:
                    server_data['location'] = get_or_create(
                        db.session, api_models.Location, location)

                server_data['server_group_id'] = api_models.ServerQuery.find_server_group_id(
                    domain, destination)

                server = get_or_create(
                    db.session, api_models.Server, server_data)
                if domain != False:
                    domain = api_models.Domain(server=server, name=domain)
                    db.session.add(domain)
                    db.session.commit()
    def resolve_sources(self, sources):
        for source in sources:
            with self._lock:
                device_query = pihole_models.PiHoleDevice.query
                found_device = device_query.join(pihole_models.PiHoleDevice.addresses).filter(pihole_models.NetworkAddress.ip == source).first()
                if found_device:
                    db.session.query(api_models.Traffic).filter_by(src=source).update({api_models.Traffic.src: found_device.hwaddr})
                    db.session.commit()

    def get(self, cmd):
        func = getattr(self, cmd)
        if callable(func):
            return func
        else:
            utils.log("Command {} not found".format(cmd))
            return False
