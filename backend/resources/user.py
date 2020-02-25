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
from flask_login import login_user, current_user

@login_manager.user_loader
def load_user(id):
    u = User.find_by_id(id)
    if not user:
        return None
    u.id = id
    return u

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
        
        # todo : return error message if token expired
        if not token:
            return {'message': 'Expecting token_id field in request body.'}, 422
        # Validate token
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), current_app.config['GOOGLE_CLIENT_ID'])

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return {'message': 'Token provided is not from google.'}, 400

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        userid = idinfo['sub']

        new_user = User()
        new_user = user_schema.load({
            'username': idinfo['email'],
            'email': idinfo['email'],
            'first_name': idinfo['given_name'],
            'last_name': idinfo['family_name'],
            'picture_url': idinfo['picture'],
            'google_id': userid
        })

        existing_user = User.find_by_google_id(userid)

        # new user
        if not existing_user:  
            new_user.created_at = datetime.now()
            
            # Save the new user into the database
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            # success
            return None, 204

        # otherwise update user with new values
        existing_user.email = new_user.email
        existing_user.first_name = new_user.first_name
        existing_user.last_name = new_user.last_name
        existing_user.picture_url = new_user.picture_url

        # todo : make sure user is the actual user to update 
        db.session.commit()
        login_user(new_user)
        return users_schema.dump(existing_user)
