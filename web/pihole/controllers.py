# Import flask dependencies
from flask import Blueprint, jsonify, request, render_template, flash, g, session, redirect, url_for
import datetime
import pihole.helpers as pihole_helpers

from web.pihole.models import PiHoleDevice

# Import the database object from the main app module
from web import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
pihole = Blueprint('pihole', __name__, url_prefix='/pihole')

# Set the route and accepted methods
@pihole.route('/devices', methods=['GET'])
def get_devices():
    devices = PiHoleDevice.getAll()
    return jsonify({'devices' : devices})
