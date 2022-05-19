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
# This will create the database file using SQLAlchemy
db.create_all()