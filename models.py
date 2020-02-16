from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    password = db.Column(db.String(128))
    registration_time = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)
    current_pw_token = db.Column(db.Integer, nullable=False)
    revoked_tokens = db.relationship('RevokedToken', backref='user')
    forms = db.relationship('Form', backref='user')

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def verify_password(self, password):
        if not password or not self.password:
            return False
        return sha256.verify(password, self.password)

    @property
    def full_name(self):
        if self.last_name != None:
            return '{} {}'.format(self.first_name, self.last_name)

        return self.first_name