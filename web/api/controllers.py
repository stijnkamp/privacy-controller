# Import flask dependencies
from flask import Blueprint, jsonify, request, render_template, flash, g, session, redirect, url_for
import datetime

from web.pihole.models import Device as PiholeDevice
from web.api.models import Device, Traffic

# Import the database object from the main app module
from web import db

# Define the blueprint: 'auth', set its url prefix: app.url/auth
api = Blueprint('api', __name__, url_prefix='/api')

# Set the route and accepted methods
@api.route('/new-devices', methods=['GET'])
def new_devices():
    known_devices =  Device.query.all()
    device_ids = [device.pihole_device_id for device in known_devices]
    unknown_devices = PiholeDevice.get_query().filter(PiholeDevice.id.notin_(device_ids)).all()
    return jsonify({'unknown_devices' : unknown_devices})
@api.route('/traffic', methods=['GET'])
def get_traffic():
    since = datetime.datetime.now() - datetime.timedelta(hours=24) 
    traffic =  Traffic.query.filter(Traffic.date_created > since).all()
    return jsonify({'traffic' : traffic})
