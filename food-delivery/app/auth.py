from flask_restful import Resource
from webargs.flaskparser import use_args
from flask_jwt_extended import create_access_token, verify_jwt_in_request, get_jwt_claims
from flask import make_response, jsonify

from functools import wraps

from app.schemas import LoginSchema
from app.models import User
from app.utils import error_object
from app import jwt


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'role': user.role}


@jwt.user_loader_callback_loader
def user_loader_callback(email):
    return User.query.filter_by(email=email).first()


def requires_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt_claims()
            if claims['role'] != role:
                return error_object('Sorry, you do not have access to this resource', 401)
            return wrapper(*args, **kwargs)
        return wrapper
    return decorator


class LoginResource(Resource):
    @use_args(LoginSchema())
    def post(self, login_args):
        user = User.query.filter_by(email=login_args['email']).first()
        if user is None:
            return error_object('Bad username or password', 401)
        if not user.validate_password(login_args['password']):
            return error_object('Bad username or password', 401)
        access_token = create_access_token(identity=user)
        return make_response(jsonify(access_token=access_token), 200)