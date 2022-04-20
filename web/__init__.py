# Import flask and template operators
from flask import Flask, render_template
# Cors enabled for development
from flask_cors import CORS

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__, static_folder='www', static_url_path="/")
CORS(app)
# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from web.auth.controllers import auth as auth_module
from web.pihole.controllers import pihole as pihole_module
from web.api.controllers import api as api_module
# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(pihole_module)
app.register_blueprint(api_module)
# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()