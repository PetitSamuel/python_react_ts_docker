import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
import marshmallow
from marshmallow import ValidationError, Schema, fields
from flask_marshmallow import Marshmallow
from datetime import datetime
from marshmallow_sqlalchemy import field_for, auto_field, SQLAlchemyAutoSchema

db = SQLAlchemy()
ma = Marshmallow()

def init_app(app):
    db.init_app(app)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    is_admin = db.Column(db.Boolean, default=False)
    quizzes = db.relationship('Quiz', backref='user')
    questions = db.relationship('Question', backref='user')
    sessions = db.relationship('Session', backref='user')

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class Quiz(db.Model):
    __tablename__ = "quiz"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    questions = db.relationship('QuizToQuestionLink', backref='quiz')

    @classmethod
    def find_by_author_id(cls, author_id):
        return cls.query.filter_by(author_id=author_id).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_author_and_name(cls, author_id, name):
        return cls.query.filter_by(author_id=author_id, name=name).first()


class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    quizzes = db.relationship('QuizToQuestionLink', backref='question')
    votes = db.relationship('Vote', backref='question')
    sessions = db.relationship('Session', backref='question')
   
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_author_id(cls, author_id):
        return cls.query.filter_by(author_id=author_id).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class QuizToQuestionLink(db.Model):
    __tablename__ = "quiztoquestion"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    @classmethod
    def find_by_quiz_id(cls, quiz_id):
        return cls.query.filter_by(quiz_id=quiz_id).first()

    @classmethod
    def find_by_question_id(cls, question_id):
        return cls.query.filter_by(question_id=question_id).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class Vote(db.Model):
    __tablename__ = "vote"
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    vote_a = db.Column(db.Integer, default=0)
    vote_b = db.Column(db.Integer, default=0)
    vote_c = db.Column(db.Integer, default=0)
    vote_d = db.Column(db.Integer, default=0)
    started_at = db.Column(db.DateTime, default=datetime.now())

    @classmethod
    def find_by_question_id(cls, question_id):
        return cls.query.filter_by(question_id=question_id).first()

    @classmethod
    def find_by_session_id(cls, session_id):
        return cls.query.filter_by(session_id=session_id).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class Session(db.Model):
    __tablename__ = "session"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_code = db.Column(db.String(8), index=True, unique=True, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.now())

    @classmethod
    def find_by_session_code(cls, session_code):
        return cls.query.filter_by(session_code=session_code).first()

    @classmethod
    def find_by_question_id(cls, question_id):
        return cls.query.filter_by(question_id=question_id).first()

    @classmethod
    def find_by_author_id(cls, author_id):
        return cls.query.filter_by(author_id=author_id).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class SessionSchema(ma.ModelSchema):
    class Meta:
        model = Session

class QuizSchema(ma.ModelSchema):
    class Meta:
        model = Quiz
        exclude = ('author_id',)

class QuestionSchema(ma.ModelSchema):
    class Meta:
        model = Question

class QuizToQuestionLinkSchema(ma.ModelSchema):
    class Meta:
        model = QuizToQuestionLink

class VoteSchema(ma.ModelSchema):
    class Meta:
        model = Vote

user_schema = UserSchema()
users_schema = UserSchema(many=True)
session_schema = SessionSchema()
sessions_schema = SessionSchema(many=True)
quiz_schema = QuizSchema()
quizzes_schema = QuizSchema(many=True)
question_schema = QuestionSchema()
questions_schema = QuestionSchema(many=True)
quiztoquestion_schema = QuizToQuestionLinkSchema()
quiztoquestions_schema = QuizToQuestionLinkSchema(many=True)
vote_schema = VoteSchema()
votes_schema = VoteSchema(many=True)
