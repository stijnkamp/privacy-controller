from flask import jsonify, request
import jwt
from functools import wraps
import datetime
import config

# Import module models (i.e. User)
from web.auth.models import User

def optional_arg_decorator(fn):
    def wrapped_decorator(*args):
        if len(args) == 1 and callable(args[0]):
            return fn(args[0])

        else:
            def real_decorator(decoratee):
                return fn(decoratee, *args)

            return real_decorator

    return wrapped_decorator

@optional_arg_decorator
def token_required(f, get_user=None):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return jsonify({'message': 'a valid token is missing'}), 401
        try:
            data = jwt.decode(token, config.auth['SECRET_KEY'], algorithms=["HS256"])
            if(get_user):
                args[0].state.user = User.query.filter_by(email=data['email']).first()
        except Exception as e:
            return jsonify({'message': 'token is invalid'}), 401

        return f(*args, **kwargs)
    return decorator
