import os
from resolver.helpers import get_database_file
import utils
# Statement for enabling the development environment

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

#All configuration that will be added to the flask server
flask = {
    'DEBUG': False,
    'PORT': 8888,
    'HOST': '0.0.0.0',
    'BASE_DIR': BASE_DIR,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///' + os.path.join(BASE_DIR, 'database.db'),
    'SQLALCHEMY_BINDS': {
        'pihole': 'sqlite:///' + get_database_file()
    },
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'CSRF_ENABLED': True,
    'CSRF_SESSION_KEY': '8bdeee308efb2c13f58ad5167acd4652'
}
#Authentication salt
auth = {
    'SECRET_KEY': 'cde1ae1a87d3a2b8560174fa7e77ca20'
}
#Settings for the websocket server
websocket = {
    'PORT': 8001,
    'HOST': '0.0.0.0'
}

hostname = 'private-home'

#How far do we want to track the traffic
#options: 'src', 'dst', 'proto', 'service'
packet_granularity = 'dst'

def get_service(service):
    """Get a specific service from its folder

    Args:
        service (str): service slug from services folder

    Returns:
        dict: Service configurations
    """
    file_path = f'config/services/{service}/configuration.json'
    service_configuration = utils.get_json(file_path)
    return service_configuration

def get_services():
    """Walk through ``config/services`` folder to detect all services

    Returns:
        list: list with all services
    """
    services = []
    path = utils.get_path('config/services')
    for entry in os.scandir(path):
        if(entry.is_dir()):
            service = get_service(entry.name)
            if service:
                services.append(service)
    return services