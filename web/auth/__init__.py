from web.auth.controllers import AuthView

class Auth(object):
    def __init__(self, state):
        self.state = state

    def register(self, app):
        AuthView.register(
            app, init_argument=self.state)
