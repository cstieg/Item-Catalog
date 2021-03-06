"""Login handler"""
import logging
import flask
from functools import wraps

from itemcatalog import app

@app.route('/login', methods=['GET'])
def login_handler():
    """Render login page"""
    return flask.render_template('login.html')

def check_logged_in(func):
    """Decorator to check whether user is logged in.  If not logged in, redirects
    to login page.
    
    Usage:
    @app.route(.....)
    @check_logged_in
    def xxx_handler():
        etc.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return func(*args, **kwargs)
        else:
            logging.info('redirecting to login')
            return flask.redirect(flask.url_for('login_handler'))
    return wrapper
