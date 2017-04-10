import logging
import flask
from google.appengine.ext import db
from google.appengine.api import users
from functools import wraps

# TODO: Add validators for entity fields

def check_signed_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return func(*args, **kwargs)
        else:
            logging.info('redirecting to signin')
            return flask.redirect('/signin')
    return wrapper


class User(db.Model):
    """Users registered to create content and comment and like on the blog"""
    username = db.StringProperty(required=True, indexed=True)
    full_name = db.StringProperty()
    password = db.StringProperty()
    signedUp = db.DateTimeProperty(auto_now_add=True, indexed=True)
    email = db.EmailProperty(indexed=True)
    provider = db.StringProperty(indexed=True)
    picture = db.URLProperty()

def find_user_by_email(email):
    user_search = User.all()
    user_search.filter('email = ', email)
    return user_search.get(read_policy=db.STRONG_CONSISTENCY)

def create_user(email, name, provider, picture):
    existing_user = find_user_by_email(email)
    if existing_user and existing_user.email != email:
        return None
    new_user = User(username=email,
                    full_name=name,
                    email=email,
                    provider=provider,
                    picture=picture)

    return new_user
