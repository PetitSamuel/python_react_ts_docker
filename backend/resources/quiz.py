from flask_restful import Resource
from flask import request
from os import environ
from datetime import datetime
from marshmallow import ValidationError

from . import json_required
from models import *

class QuizAPi(Resource):
    @json_required
    def post(self):
        new_quiz = Quiz()
        try:
            new_quiz = quiz_schema.load(request.r_data)
        except ValidationError as err:
            return err.messages, 422
        if Quiz.find_by_author_and_name(new_quiz.author_id, new_quiz.name):
            return {'message': 'Quiz {} - already exists for user'.format(new_quiz.name)}, 400
        # todo : make sure user exists ?
        # todo : set author_id here 
        new_quiz.author_id = 1 
        new_quiz.created_at = datetime.now()

        # Save the new user into the database
        db.session.add(new_quiz)
        db.session.commit()
        # success
        return None, 204


    # PATCH -> Rename a quiz
    @json_required
    def patch(self):
        # Validate and deserialize input
        received_quiz = Quiz()
        try:
            received_quiz = quiz_schema.load(request.r_data, session=db.session)
        except ValidationError as err:
            return err.messages, 422

        if not received_quiz.id:
            return {'message': 'No id provided'}, 400
        to_update = Quiz.find_by_id(received_quiz.id)
        if not to_update:
            return {'message': 'Form {} does not exist'.format(to_update.id)}, 400
        
        # todo : make sure user is the actual user to update 
        to_update.name = received_quiz.name
        db.session.commit()
        return quiz_schema.dump(to_update)