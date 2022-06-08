# Import flask and template operators
from flask import Flask
# Cors enabled for development
from flask_cors import CORS
# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import config



# Define the WSGI application object
app = Flask(__name__, static_folder='www', static_url_path="/")

# Setup CORS rules
CORS(app)

# Configurations
app.config.update(config.flask)

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
# Build the database:
from web.api import models as api_models
from web.pihole import models as pihole_models
# This will create the database file using SQLAlchemy
db.create_all()