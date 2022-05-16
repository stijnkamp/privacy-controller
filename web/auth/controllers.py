# Import flask dependencies
from flask import Blueprint, jsonify, request, render_template, flash, g, session, redirect, url_for
import jwt
# Import password / encryption helper tools
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import datetime
import config as config


# Import the database object from the main app module
from web import db

# Import module models (i.e. User)
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


# Define the blueprint: 'auth', set its url prefix: app.url/auth
auth = Blueprint('auth', __name__, url_prefix='/auth')

# Set the route and accepted methods


@auth.route('/token', methods=['POST'])
def token():
    requestData = request.json
    user = User.query.filter_by(email=requestData['email']).first()

    if user and check_password_hash(user.password, requestData['password']):

        token = jwt.encode({'email': user.email, 'exp': datetime.datetime.utcnow(
        ) + datetime.timedelta(minutes=120)}, config.SECRET_KEY, "HS256")
        extra = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
        return jsonify({'token': token})

    return jsonify({'error': "Credentials incorrect"})
