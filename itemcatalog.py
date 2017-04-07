import logging
import os
from flask import Flask
import signup


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['static'] = os.path.join(APP_ROOT, 'static')

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/signup')
def signup_handler():
    logging.info("here")
    return signup.signup()

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500, 500
