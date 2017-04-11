import logging
import os
import flask
import random
import string

app = flask.Flask(__name__)
app.secret_key = 'ZAwsBF5SZD6#QzwRnDvakmJ5xp4d7XqRaxX#^V!T'

import gconnect
import login
import logout

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
@login.check_signed_in
def main_page_handler():
    username = flask.session.get('username')
    return flask.render_template('index.html', username=username)

@app.route('/signup')
def signup_handler():
    if flask.request.method == 'GET':
        return flask.render_template('signup.html')

@app.route('/login')
def login_handler():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')

@app.route('/logout')
def logout_handler():
    return logout.logout()


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500, 500
