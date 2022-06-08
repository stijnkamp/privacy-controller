from web import db
import web.api.models as api_models
from web.pihole import models as pihole_models
from web.helpers import get_or_create
import multiprocessing
import utils
import time
from resolver import dns_lookup


class ResolverCommands(object):
    def __init__(self):
        self._lock = multiprocessing.Lock()

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
            start = time.time()
            domain = dns_lookup.get_domain_for_ip(destination)
            location = dns_lookup.get_location_for_ip(destination)
            company = dns_lookup.get_company_for_domain(domain)
            with self._lock:
                server_data = {
                    'ip': destination
                }

                if company != None:
                    server_data['company'] = get_or_create(
                        db.session, api_models.Company, {"name":company})
                if location != False:
                    server_data['location'] = get_or_create(
                        db.session, api_models.Location, location)

                server_data['server_group_id'] = api_models.ServerQuery.find_server_group_id(destination, domain, company)
                server = get_or_create(
                    db.session, api_models.Server, server_data)
                if domain != False:
                    domain = api_models.Domain(server=server, name=domain)
                    db.session.add(domain)
                    db.session.commit()
    def resolve_sources(self, sources):
        for source in sources:
            source = source.replace('ip-', '')
            with self._lock:
                device_query = pihole_models.PiHoleDevice.query
                found_device = device_query.join(pihole_models.PiHoleDevice.addresses).filter(pihole_models.NetworkAddress.ip == source).first()
                if found_device:
                    db.session.query(api_models.Traffic).filter_by(src=source).update({api_models.Traffic.src: found_device.hwaddr})
                    db.session.commit()
    def check_all_sources(self):
        sources = db.session.query(api_models.Traffic.src).filter(api_models.Traffic.src.contains('192.168.2.')).group_by(api_models.Traffic.src).all()
        sources = set(map(lambda traffic: traffic.src, sources))
        self.resolve_sources(sources)

    def get(self, cmd):
        func = getattr(self, cmd)
        if callable(func):
            return func
        else:
            utils.log("Command {} not found".format(cmd))
            return False
