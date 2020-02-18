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

class Question(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    quizzes = db.relationship('QuizToQuestionLink', backref='question')
    votes = db.relationship('Vote', backref='question')
    sessions = db.relationship('Session', backref='question')

class QuizToQuestionLink(db.Model):
    __tablename__ = "quiztoquestion"
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

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

class Session(db.Model):
    __tablename__ = "session"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    session_code = db.Column(db.String(8), index=True, unique=True, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.now())

class SessionSchema(ma.ModelSchema):
    class Meta:
        model = Session

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User

class QuizSchema(ma.ModelSchema):
    class Meta:
        model = Quiz

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
