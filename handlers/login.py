"""Login handler"""
import logging
import flask

from flaskapp import app

@app.route('/login', methods=['GET'])
def login_handler():
    """Render login page"""
    return flask.render_template('login.html')

