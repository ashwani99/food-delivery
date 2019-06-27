from flask import jsonify, make_response
from webargs.flaskparser import parser, abort
from flask_jwt_extended import current_user, get_jwt_claims

from functools import wraps

from .models import Role

def error_object(msg, httpcode):
    return make_response(jsonify(error=msg), httpcode)


@parser.error_handler
def handle_request_parsing_error(err, req, schema, status_code, headers):
    abort(status_code, errors=err.messages)


# def requires_role(role):
#     def decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             claims = get_jwt_claims()
#             role = claims.pop('role', None)
#             if role is None:
#                 return 
#                 return wrapper(*args, **kwargs)
#             return error_object('You do not have access to that page. Sorry!', 401)
#         return wrapper
#     return decorator