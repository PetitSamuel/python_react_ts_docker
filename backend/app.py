# compose_flask/app.py
import os
from os import environ
from datetime import datetime
from flask import Flask, Response, request, jsonify, render_template
from redis import Redis
from flask_cors import CORS

import models
from models import db, User

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
CORS(app)

# Configuration is provided through environment variables by Docker Compose
app.config.update({
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SECRET_KEY': environ['FLASK_SECRET'],
    'PREFERRED_URL_SCHEME': 'https',
    #'ROOT_EMAIL': environ['ROOT_EMAIL'],
    #'RATELIMIT_ENABLED': True if environ['FLASK_ENV'] == 'production' else False,
    # Database 0 is for ratelimiting
    #'RATELIMIT_STORAGE_URL': 'redis://redis:6379/0',
    # Database 1 is for background tasks
    #'CELERY_RESULT_BACKEND': 'redis://redis:6379/1',
    #'CELERY_BROKER_URL': 'redis://redis:6379/1',
})

app.config.update({
    'SQLALCHEMY_DATABASE_URI': 'mysql+mysqlconnector://{user}:{password}@{host}/{database}'.format(
        user = environ['MYSQL_USER'],
        password = environ['MYSQL_PASSWORD'],
        host = environ['MYSQL_HOST'],
        database = environ['MYSQL_DATABASE']
    ),
})

@app.errorhandler(404)
def not_found(e):
    if request.path.startswith('/api/v1'):
        return jsonify({'message': 'Not found'}), 404

    return '404 : not found'

models.init_app(app)

@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')

@app.before_first_request
def init_db():
    # Create the tables (does nothing if they already exist)
    db.create_all()

    # Create the default `root` user if they don't exist
    root = User.find_by_username('root')
    if not root:
        print('**** NO ROOT USER FOUND ****')
    print(root)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)