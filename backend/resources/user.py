from flask_restful import Resource
from flask import request, jsonify, current_app
from os import environ
from datetime import datetime
from marshmallow import ValidationError
from google.oauth2 import id_token
from google.auth.transport import requests
import json
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

class GoogleAuthAPI(Resource):
    @json_required
    def post(self):
        token = request.json['token_id']
        idinfo = None


        # Validate token
        try:
            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), current_app.config['GOOGLE_CLIENT_ID'])

            # Or, if multiple clients access the backend server:
            # idinfo = id_token.verify_oauth2_token(token, requests.Request())
            # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
            #     raise ValueError('Could not verify audience.')

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # If auth request is from a G Suite domain:
            # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
            #     raise ValueError('Wrong hosted domain.')

            # ID token is valid. Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']
        except ValueError:
            # Invalid token
            return {'message': 'an error occured with google verification'}, 400

        new_user = User()
        new_user = user_schema.load({
            'username': idinfo['email'],
            'email': idinfo['email'],
            'first_name': idinfo['given_name'],
            'last_name': idinfo['family_name'],
            'picture_url': idinfo['picture']
        })
        new_user.created_at = datetime.now()
        
        # Save the new user into the database
        db.session.add(new_user)
        db.session.commit()
        # success
        return None, 204
