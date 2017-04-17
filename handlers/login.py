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
    logging.info(flask.session.get('email'))
    return user_login.find_user_by_email(flask.session.get('email'))

def check_logged_in(func):
    logging.info(func)
    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(args)
        logging.info(flask.session.get('username'))
        if 'username' in flask.session:
            return func(*args, **kwargs)
        else:
            logging.info('redirecting to login')
            return flask.redirect(flask.url_for('login_handler'))
    return wrapper