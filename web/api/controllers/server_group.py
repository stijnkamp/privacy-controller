import datetime
from flask import jsonify
from flask_classful import route
from web.controller import Controller
from web.api import models as api_models
from web.pihole import models as pihole_models
from web.helpers import get_input, parse_model
from web import db
from web.auth.helpers import token_required


class ServerGroupView(Controller):
    decorators = [token_required]
    route_base = '/server-groups'
    @route('<id>', methods=['GET'])
    def get(self, id):
        if id == 'unknown':
            servers = api_models.Server.query.filter(api_models.Server.server_group_id == None).all()
            unknown_server_group = {
                'name': 'Unknown',
                'servers': servers
            }
            return jsonify({'server_group': unknown_server_group})
        server_group = api_models.ServerGroup.query.get(id)
        response = parse_model(server_group)
        services = server_group.services
        data_types = set()
        for service in services:
            data_types = data_types.union(set(map(lambda data: data.data_type_id, service.service_data)))
        relation_filter = ~api_models.Abstraction.needed_data_types.any(~api_models.DataType.id.in_(data_types))
        response['abstractions'] = api_models.Abstraction.query.filter(relation_filter).all()
        response['services'] = []
        response['servers'] = api_models.Server.query.filter(api_models.Server.server_group_id == id).all()
        for index, service in enumerate(services):
            functionalities = parse_model(service.functionalities)
            filteredFunctionalities = []
            for index, functionality in enumerate(functionalities):
                del functionality['services']
                functionality['devices'] = list(map(lambda device: device.name, service.functionalities[index].devices))
                if len(functionality['devices']) > 0:
                    filteredFunctionalities.append(functionality)
            if len(filteredFunctionalities) > 0:
                active_service = parse_model(service)
                active_service['functionalities'] = filteredFunctionalities
                response['services'].append(active_service)
            
        return jsonify({'server_group': response})