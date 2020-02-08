# compose_flask/app.py
from flask import Flask, jsonify
from redis import Redis
from flask_cors import CORS

app = Flask(__name__)
redis = Redis(host='redis', port=6379)
CORS(app)

@app.route('/')
def hello():
    redis.incr('hits')
    return 'This Compose/Flask demo has been viewed %s time(s).' % redis.get('hits')

@app.route('/test')
def test():
    return jsonify(result="hello my test!")

@app.route('/session/<id>')
def session(id):
    print(id)
    return jsonify(
        sessionInfo="Welcome to session %s" % id,
        other="cool"
    )
@app.route('/set_session/<id>')
def incrSession(id):
    redis.incr("%s" % id)
    print(id)
    print('number: %s times' % redis.get('%s' % id))
    return 'this sessions has been viewed %s time(s).' % redis.get('%s' % id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)