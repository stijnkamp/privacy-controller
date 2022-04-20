from flask import Flask
import utils
import config
import threading
from flask import Flask, jsonify, make_response, request
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import uuid
import jwt
import datetime
from web import app
from web.auth.models import User

def token_required(f):
   @wraps(f)
   def decorator(*args, **kwargs):
       token = None
       if 'Authorization' in request.headers:
           token = request.headers['Authorization']
       if not token:
           return jsonify({'message': 'a valid token is missing'})
       try:
           data = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
           current_user = User.query.filter_by(email=data['email']).first()
       except:
           return jsonify({'message': 'token is invalid'})
 
       return f(current_user, *args, **kwargs)
   return decorator

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return app.send_static_file("index.html")
    
class WebServer(object):
    def __init__(self, state):
        self._lock = threading.Lock()
        self._active = False
        self._thread = threading.Thread(target=self._web_server_monitor)
        self._thread.daemon = True
    def start(self):
            with self._lock:
                self._active = True
            utils.log('[Web Server] Starting.')
            self._thread.start()
    
    def _web_server_monitor(self):
        utils.restart_upon_crash(app.run, kwargs={'port': config.PORT, 'host': '0.0.0.0'})