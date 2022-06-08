# Import flask dependencies
from flask import Blueprint, jsonify, request, render_template, flash, g, session, redirect, url_for
import jwt
from flask_classful import route
# Import password / encryption helper tools
from werkzeug.security import check_password_hash
from functools import wraps
import datetime
import config
from web.auth.helpers import token_required

from web.controller import Controller

# Import module models (i.e. User)
from web.auth.models import User

# Set the route and accepted methods
class AuthView(Controller):
    decorators = []

    @route('/token', methods=['POST'])
    def token(self):
        requestData = request.json
        user = User.query.filter_by(email=requestData['email']).first()

        if user and check_password_hash(user.password, requestData['password']):

            token = jwt.encode({'email': user.email, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(minutes=120)},config.auth['SECRET_KEY'], "HS256")
            extra = jwt.decode(token, config.auth['SECRET_KEY'], algorithms=["HS256"])
            return jsonify({'token': token})

        return jsonify({'error': "Credentials incorrect"}), 401

    @route('/me', methods=['GET'])
    @token_required(True)
    def me(self):
        return jsonify({'user': self.state.user})
        
