from flask_restful import Resource
from flask import request
from os import environ
from datetime import datetime
from marshmallow import ValidationError

from . import json_required
from models import *

class QuestionAPI(Resource):
    #todo handle multiple question submission ?
    @json_required
    def post(self):
        new_quiz = Question()
        try:
            new_question = question_schema.load(request.r_data)
        except ValidationError as err:
            return err.messages, 422
        if Question.find_by_author_id_and_text(new_quiz.author_id, new_quiz.text):
            return {'message': 'Question {} - already exists for user'.format(new_quiz.text)}, 400
      
        # todo : make sure user exists ?
        # todo : set author_id here 
        new_question.author_id = 1 
        new_question.created_at = datetime.now()

        # Save the new quiz into the database
        db.session.add(new_question)
        db.session.commit()
        # success
        return None, 204

    # PATCH -> Change question text
    @json_required
    def patch(self):
        received_question = Question()
        try:
            received_question = question_schema.load(request.r_data, session=db.session)
        except ValidationError as err:
            return err.messages, 422

        if not received_question.id:
            return {'message': 'No id provided'}, 400
            # todo : also use author id here
        to_update = Question.find_by_id(received_question.id)
        if not to_update:
            return {'message': 'Question id {} does not exist'.format(received_question.id)}, 400
        
        # todo : make sure user is the actual user to update 
        to_update.text = received_question.text
        db.session.commit()
        return question_schema.dump(to_update)

    # delete -> delete question
    @json_required
    def delete(self):
        del_question = Question()
        try:
            del_question = delete_question_schema.load(request.r_data, session=db.session)
        except ValidationError as err:
            return err.messages, 422

        to_delete = Question.find_by_id(del_question.id)
        if not to_delete:
            return {'message': 'Question {} does not exist'.format(del_question.id)}, 400

        # todo : make sure user is doing the thing
        #if not current_user.is_admin and to_delete.user != current_user:
        #    return {'message': ('You must have either submitted form {} '
        #            'or be an admin to delete it').format(to_delete.id)}, 401

        db.session.delete(to_delete)
        db.session.commit()
        return None, 204
