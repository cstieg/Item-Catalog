import logging
import os
import flask
import random
import string
from google.appengine.api.backendinfo import STATE

app = flask.Flask(__name__)
app.secret_key = 'ZAwsBF5SZD6#QzwRnDvakmJ5xp4d7XqRaxX#^V!T'

import gconnect
import login

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@login.check_signed_in
def hello():
    username = flask.session.get('username')
    return 'Hello, %s!' % username

@app.route('/signup')
def signup_handler():
    if flask.request.method == 'GET':
        return flask.render_template('signup.html', user='')

@app.route('/signin')
def signin_handler():
    if flask.request.method == 'GET':
        return flask.render_template('signin.html')

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500, 500


def set_state():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    flask.session['state'] = state
    return state
