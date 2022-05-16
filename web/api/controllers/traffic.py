import datetime
from flask import jsonify
from flask_classful import route
from web.controller import Controller
from web.api import models as api_models
from web.pihole import models as pihole_models
from web.helpers import get_input, parse_model
from web import db


class TrafficView(Controller):
    excluded_methods = ['get_sources', 'get_destinations']

    @route('', methods=['POST'])
    def index(self):
        filter = get_input()
        since = datetime.datetime.now() - datetime.timedelta(weeks=1)
        till = datetime.datetime.now()
        group_by = filter['group_by'] if 'group_by' in filter else 'src'
        if 'date' in filter:
            since = datetime.datetime.fromisoformat(
                filter['date'][0].replace('Z', ''))
            since = since.replace(hour=0, minute=0)
            till = datetime.datetime.fromisoformat(
                filter['date'][1].replace('Z', ''))
            till = till.replace(hour=23, minute=59)
        group_data_formats = {
            'day': '%Y-%m-%d %H:%M',
            'week': '%Y-%m-%d %H',
            'month': '%Y-%m-%d',
            'year': '%Y-%m',
        }
        group_date_format = '%Y-%m-%d %H:%M'
        if 'duration' in filter and filter['duration'] in group_data_formats:
            group_date_format = group_data_formats[filter['duration']]
        traffic_query = db.session.query(api_models.Traffic, db.func.sum(api_models.Traffic.size).label('size_total'), db.func.strftime(
            group_date_format, api_models.Traffic.date_created).label('date_group'))
        traffic_query = traffic_query.filter(api_models.Traffic.date_created > since).filter(
            api_models.Traffic.date_created <= till)
        if 'devices' in filter:
            devices = api_models.Device.query.filter(
                api_models.Device.id.in_(filter['devices'])).all()
            deviceMacs = list(map(lambda device: device.hwaddr, devices))
            traffic_query = traffic_query.filter(
                api_models.Traffic.src.in_(deviceMacs))
        traffic_query = traffic_query.group_by(
            getattr(api_models.Traffic, group_by), 'date_group')
        print(traffic_query.statement.compile(
            compile_kwargs={"literal_binds": True}))

        def parse_result(trafficData):
            trafficData = parse_model(trafficData)
            traffic = trafficData['Traffic']
            traffic['date_created'] = trafficData['date_group']
            traffic['size'] = trafficData['size_total']
            return traffic
        traffic = list(map(parse_result, traffic_query.all()))
        devices = self.get_sources(traffic_query)
        servers = self.get_destinations(traffic_query)
        return jsonify({'traffic': traffic, 'devices': devices, 'servers': servers})

    def get_sources(self, query):
        mac_addresses = query.group_by('src').all()
        mac_addresses = set(
            map(lambda traffic: traffic.Traffic.src, mac_addresses))
        devices = pihole_models.PiHoleDevice.get_query().filter(
            pihole_models.PiHoleDevice.hwaddr.in_(mac_addresses)).all()
        devices = parse_model(devices)

        # Retrieve known device
        def get_known_device(pihole_device):
            device = api_models.Device.query.filter(
                api_models.Device.pihole_device_id == pihole_device['id']).first()
            pihole_device['device'] = device
            return pihole_device
        devices = list(map(get_known_device, devices))
        return devices

    def get_destinations(self, query):
        ip_addresses = query.group_by('dst').all()
        ip_addresses = set(
            map(lambda traffic: traffic.Traffic.dst, ip_addresses))
        servers = api_models.Server.query.filter(
            api_models.Server.ip.in_(ip_addresses)).all()
        return servers
