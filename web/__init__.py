# Import flask and template operators

from flask import Flask, request, jsonify, url_for
# Cors enabled for development
from flask_cors import CORS

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import utils
import multiprocessing
import config as config

# Define the WSGI application object
app = Flask(__name__, static_folder='www', static_url_path="/")

# Setup CORS rules
CORS(app)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

# Register the general application
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")

from web.api import Api

class WebServer(object):
    def __init__(self, state):
        self._lock = multiprocessing.Lock()
        self._active = False
        self._thread = multiprocessing.Process(target=self._web_server_monitor)
        self._thread.daemon = True
        self.state = state
        self.setup_modules()

    def setup_modules(self):
        modules = [Api(self.state)]
        for module in modules:
            module.register(app)

    def start(self):
        with self._lock:
            self._active = True
        utils.log('[Web Server] Starting.')
        self._thread.start()

    def _web_server_monitor(self):
        utils.restart_upon_crash(
            app.run, kwargs={'port': config.PORT, 'host': '0.0.0.0'})

    def stop(self):
        with self._lock:
            self._thread.terminate()
        self._thread.join()
        utils.log('[Web server] Stopped.')
