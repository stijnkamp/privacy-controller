from flask_classful import FlaskView
class Controller(FlaskView):
    def __init__(self, state):
        self.state = state