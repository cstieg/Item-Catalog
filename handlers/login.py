import logging
import flask
from functools import wraps
from models import user_login
from itemcatalog import app


@app.route('/signup', methods=['GET'])
def signup_handler():
    return flask.render_template('signup.html')

@app.route('/login', methods=['GET'])
def login_handler():
    return flask.render_template('login.html')

def get_current_user():
    return user_login.find_user_by_email(flask.session.get('email'))

def check_logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return func(*args, **kwargs)
        else:
            logging.info('redirecting to login')
            return flask.redirect(flask.url_for('login_handler'))
    return wrapper