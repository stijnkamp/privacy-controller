from web.api.controllers import devices, traffic
from flask_classful import FlaskView

class Api(object):
    def __init__(self, state):
        self.state = state

    def register(self, app):
        devices.DevicesView.register(
            app, init_argument=self.state, route_prefix='api')
        traffic.TrafficView.register(
            app, init_argument=self.state, route_prefix='api')
