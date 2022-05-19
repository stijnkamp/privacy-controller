import utils
import config
import os
import shutil
from web import helpers as web_helpers
from web import db
import web.api.models as api_models

    
def setup():
    utils.log("Setting up all services")
    utils.log("Set hostname to {}.local".format(config.hostname))
    set_hostname(config.hostname)
    services = config.get_services()
    update_services_in_database(services)

def update_services_in_database(services):
    server_groups = {}
    data_types = {}
    device_types = {}
    device_type_models = {}
    {
      "slug": "bridge",
      "name": "Philips Hue Bridge",
      "icon": "hue_bridge.png",
      "functionalities": [
        {
          "name": "Control using the dedicated app",
          "services": [
            {
              "slug": "send_status_to_hue_cloud",
              "server_group": "philips.philips_hue_servers",
              "data": [
                {
                  "type": "philips.lamp_status",
                  "trigger": "Every 10 seconds"
                }
              ]
            }
          ]
        },
        {
          "name": "Control by Google Voice Command",
          "services": [
            {
              "slug": "send_status_to_google_servers",
              "server_group": "philips.philips_hue_servers",
              "data": [
                {
                  "type": "philips.lamp_status",
                  "trigger": "Every 10 seconds"
                }
              ]
            }
          ]
        }
      ]
    }
    # server_groups = [web_helpers.get_input(['name', 'slug'], service_alliance.server_groups) for service_alliance in services]
    for service_alliance in services:
        if 'data_types' in service_alliance:
            for data_type in service_alliance['data_types']:
                data_type['slug'] = f'{service_alliance["slug"]}.{data_type["slug"]}'
                data_types[data_type['slug']] = data_type
        
        if 'server_groups' in service_alliance:
            for server_group in service_alliance['server_groups']:
                server_group['slug'] = f'{service_alliance["slug"]}.{server_group["slug"]}'
                server_groups[server_group['slug']] = server_group
        
        if 'device_types' in service_alliance:
            for device_type in service_alliance['device_types']:
                device_type['slug'] = f'{service_alliance["slug"]}.{device_type["slug"]}'
                device_type['icon'] = copy_icon(service_alliance['slug'], device_type['icon'])
                device_types[device_type['slug']] = device_type
    
    for data_type_slug in data_types:
        data_type_data = data_types[data_type_slug]
        query = {'slug': data_type_data['slug']}
        model = web_helpers.get_input(['slug', 'name', 'icon'], data_type_data)
        data_type = web_helpers.update_or_create(db.session, api_models.DataType, query, model)
        data_types[data_type_slug] = data_type
    
    for server_group_slug in server_groups:
        server_group_data = server_groups[server_group_slug]
        query = {'slug': server_group_data['slug']}
        model = web_helpers.get_input(['slug', 'name'], server_group_data)
        server_group = web_helpers.update_or_create(db.session, api_models.ServerGroup, query, model)
        server_groups[server_group_slug] = server_group
    
    for device_type_slug in device_types:
        device_type_data = device_types[device_type_slug]
        query = {'slug': device_type_data['slug']}
        model = web_helpers.get_input(['slug', 'name', 'icon'], device_type_data)
        device_type = web_helpers.update_or_create(db.session, api_models.DeviceType, query, model)
        device_type_models[device_type_slug] = device_type
    
    for device_type_slug in device_types:
        device_type = device_types[device_type_slug]
        for functionality_data in device_type['functionalities']:
            functionality_model = {
                "device_type_id": device_type_models[device_type_slug].id,
                "name": functionality["name"],
            }
            functionality = web_helpers.update_or_create(db.session, api_models.Functionality, functionality_model)
            for service_data in functionality_data["services"]:
                create_service(functionality, service_data, device_types, server_groups, data_types)

        
def create_service(functionality, service, device_types, server_groups, data_types):
    service_data = {
        'slug': service['slug'],
        'device_type_id': device_types[service['device_type']].id if (service['device_type'] and service['device_type'] in device_types) else None,
        'server_group_id': server_groups[service['server_group']].id if ('server_group' in service and service['server_group'] in server_groups) else None,
        'cloud': 'server_group' in service and service['server_group'] != None
    }
    service_model = web_helpers.update_or_create(db.session, api_models.Service, service_data)
    for data in service['data']:
        if data['trigger'] in data_types:
            data["data_type_id"] = data_types[data['trigger']].id
            service_model['service_id'] = service_model.id
            data_data = web_helpers.get_input(['service_id', 'data_type_id', 'storage', 'trigger'])
            data = web_helpers.update_or_create(db.session, api_models.ServiceData, data_data)
    functionality.services.add(service)
    db.session.commit()
    
def copy_icon(device_alliance_slug, icon):
    source_path = utils.get_path('config/services/{}/assets/{}'.format(device_alliance_slug, icon))
    destination_path = utils.get_path('web/www/img/services/{}'.format(device_alliance_slug))
    os.makedirs(destination_path, exist_ok=True)
    if os.path.isfile(source_path):
        shutil.copy(source_path, destination_path)
        return '/img/services/{}/{}'.format(device_alliance_slug, icon)
    return None

def set_hostname(hostname):
    with open('/etc/hosts', 'r') as file:
        # read a list of lines into data
        data = file.readlines()

    # find line with 127.0.1.1 and replace it.
    index = [idx for idx, l in enumerate(data) if '127.0.1.1' in l][0]
    # so this replaces that line with the new hostname
    data[index] = '127.0.1.1       ' + hostname

    # save the file temporarily because /etc/hosts is protected
    with open('temp.txt', 'w') as file:
        file.writelines( data )

    # use sudo command to overwrite the protected file
    os.system('sudo mv temp.txt /etc/hosts')

    # repeat process with other file
    with open('/etc/hostname', 'r') as file:
        data = file.readlines()

    data[0] = hostname

    with open('temp.txt', 'w') as file:
        file.writelines( data )

    os.system('sudo mv temp.txt /etc/hostname')
