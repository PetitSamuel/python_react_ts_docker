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
    full_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    locality = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    is_admin = db.Column(db.Boolean, default=False)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
    
    
user_schema = UserSchema()
users_schema = UserSchema(many=True)
