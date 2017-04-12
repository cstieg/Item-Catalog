import logging
import flask
from models import user_login

def get_current_user():
    return user_login.find_user_by_email(flask.session.get('email'))