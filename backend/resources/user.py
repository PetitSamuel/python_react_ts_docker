from flask_restful import Resource
from flask import request, jsonify
from os import environ
from datetime import datetime
from marshmallow import ValidationError

from . import json_required
from models import *

class UserAPI(Resource):
    @json_required
    def post(self):
        new_user = User()
        try:
            new_user = user_schema.load(request.r_data)
        except ValidationError as err:
            return err.messages, 422
        if User.find_by_username(new_user.username):
            return {'message': 'User {} already exists'.format(new_user.username)}, 400
        if User.find_by_email(new_user.email):
            return {'message': 'A user with email {} already exists'.format(new_user.email)}, 400

        new_user.created_at = datetime.now()

        # Save the new user into the database
        db.session.add(new_user)
        db.session.commit()
        # success
        return None, 204
