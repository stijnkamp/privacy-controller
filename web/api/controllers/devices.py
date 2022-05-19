from flask import jsonify, request
from flask_classful import route
from web.controller import Controller
from web.api import models as api_models
from web.pihole import models as pihole_models
from web.helpers import get_input, add_relationship
from web import db


class DevicesView(Controller):

    def index(self):
        device_query = api_models.Device.query
        accepted_device_query = device_query.outerjoin(api_models.Device.rules).filter(
            db.or_(api_models.Rule.service != 'block', ~api_models.Device.rules.any()))
        blocked_device_query = device_query.join(
            api_models.Device.rules).filter(api_models.Rule.service == 'block')
        devices = accepted_device_query.all()
        blocked_devices = blocked_device_query.all()
        return jsonify({'devices': devices, 'blocked': blocked_devices})

    def get(self, id):
        device = api_models.Device.query.get(id)
        return jsonify({'device': device})

    def types(self):
        device_types = api_models.DeviceType.query.all()
        args = request.args
        if 'include' in args and args['include'] == 'functionalities':

            device_types = list(map(lambda device_type: add_relationship(
                device_type, 'functionalities'), device_types))
        return jsonify({'device_types': device_types})

    @route('/types/<id>/functionalities', methods=['GET'])
    def type_functionalities(self, id):
        device_type = api_models.DeviceType.query.get(id)
        return jsonify({'functionalities': device_type.functionalities})

    @route('/new', methods=['GET'])
    def new_devices(self):
        known_devices = api_models.Device.query.all()
        device_ids = [device.pihole_device_id for device in known_devices]
        new_devices = pihole_models.PiHoleDevice.get_query().filter(
            pihole_models.PiHoleDevice.id.notin_(device_ids)).all()
        return jsonify({'new_devices': new_devices})

    @route('/new/<id>', methods=['GET'])
    def new_device(self, id):
        new_device = pihole_models.PiHoleDevice.query.get(id)
        return jsonify({'new_device': new_device})

    @route('/add', methods=['POST'])
    def post(self):
        device_data = get_input(['name', 'pihole_device_id', 'device_type_id'])
        # Remove device if it existed
        existing = api_models.Device.query.filter(
            api_models.Device.pihole_device_id == device_data['pihole_device_id']).first()
        if(existing != None):
            db.session.delete(existing)
        new_device = api_models.Device(**device_data)
        request_data = get_input(['rules', 'functionalities'])
        if('rules' in request_data):
            for rule in request_data['rules']:
                new_device.rules.append(api_models.Rule(**rule))
        if('functionalities' in request_data):
            for functionality_id in request_data['functionalities']:
                new_device.functionalities.append(
                    api_models.Functionality.query.get(functionality_id))
        # for rule in date['rules']:
        #     new_device.rules.append(Rule(**rule))
        db.session.add(new_device)
        db.session.commit()
        self.state.send_command('Firewall', {
            'cmd': 'set_standard_rules'
        })
        return jsonify({'added': new_device})
