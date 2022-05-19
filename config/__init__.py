import os
import resolver.helpers as resolver_helpers
import utils
# Statement for enabling the development environment

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

flask = {
    'DEBUG': False,
    'PORT': 8888,
    'HOST': '0.0.0.0',
    'BASE_DIR': BASE_DIR,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + os.path.join(BASE_DIR, 'database.db'),
    'SQLALCHEMY_BINDS': {
        'pihole': 'sqlite:///' + resolver_helpers.get_database_file()
    },
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'CSRF_ENABLED': True,
    'CSRF_SESSION_KEY': '8bdeee308efb2c13f58ad5167acd4652',
    'SECRET_KEY': 'cde1ae1a87d3a2b8560174fa7e77ca20'
}

websocket = {
    'PORT': 8001,
    'HOST': '0.0.0.0'
}

hostname = 'private-home'

packet_granularity = 'dst'

def get_service(service):
    file_path = f'config/services/{service}/configuration.json'
    service_configuration = utils.get_json(file_path)
    return service_configuration

def get_services():
    services = []
    path = utils.get_path('config/services')
    for entry in os.scandir(path):
        if(entry.is_dir()):
            service = get_service(entry.name)
            if service:
                services.append(service)
    return services