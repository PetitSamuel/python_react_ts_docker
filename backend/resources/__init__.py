from functools import wraps

from flask import request
import flask_restful

class Api(flask_restful.Api):
    def error_router(self, orig_handler, e):
        return super(Api, self).error_router(orig_handler, e)

def json_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        json = request.get_json()
        if not json:
            return {'message': 'No input data provided (or not in json format)'}, 400
        request.r_data = json
        return f(*args, **kwargs)
    return decorated_function
