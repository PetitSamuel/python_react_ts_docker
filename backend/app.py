import os
from os import environ
from datetime import datetime
from flask import Flask, Response, request, jsonify, render_template
from redis import Redis
from flask_cors import CORS
from healthcheck import HealthCheck
import models
from models import db, User, users_schema, user_schema, ma
from resources import Api, user, quiz

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
CORS(app)

# config from .env file linked through docker-compose
app.config.update({
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SECRET_KEY': environ['FLASK_SECRET'],
    'PREFERRED_URL_SCHEME': 'https',
    'ROOT_EMAIL': environ['ROOT_EMAIL'],
    'SQLALCHEMY_DATABASE_URI': 'mysql+mysqlconnector://{user}:{password}@{host}/{database}'.format(
        user = environ['MYSQL_USER'],
        password = environ['MYSQL_PASSWORD'],
        host = environ['MYSQL_HOST'],
        database = environ['MYSQL_DATABASE']
    ),
})

api = Api(app, prefix='/api')
models.init_app(app)
ma.init_app(app)

# Default to 404
@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api'):
        return jsonify({'message': 'Not found'}), 404
    return '404 : not found', 404

@app.route('/')
def hello():
    #return jsonify({"no place like": "127.0.0.1"})
    return user_schema.dumps(User.find_by_id(1))

@app.before_first_request
def init_db():
    # Create tables (does nothing if they already exist)
    db.create_all()

    # check root exists
    # todo : create if doesn't exist
    root = User.find_by_username('root')
    if not root:
        print('**** NO ROOT USER FOUND ****')
    print('*** ROOT USER FOUND ***')

def db_ok():
    return User.query.count() >= 0, "database ok"

# Set up health check
health = HealthCheck(app, '/health', success_ttl=None, failed_ttl=None)
health.add_check(db_ok)

# Mount our API endpoints
api.add_resource(user.UserAPi, '/auth/register')
api.add_resource(quiz.QuizAPi, '/quiz')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)