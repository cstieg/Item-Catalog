import logging
import flask
import decorators
import logout
import gconnect
import catalog
import models
import handlers
from itemcatalog import app

@app.route('/')
def main_page_handler():
    username = flask.session.get('username')
    catalogs = models.get_catalogs()
    return flask.render_template('index.html', username=username, catalogs=catalogs)

@app.route('/catalog/<catalog_id>')
def catalog_view_handler(catalog_id):
    return handlers.catalog_view(catalog_id)

@app.route('/signup', methods=['GET'])
def signup_handler():
    return flask.render_template('signup.html')

@app.route('/login', methods=['GET'])
def login_handler():
    return flask.render_template('login.html')

@app.route('/gconnect', methods=['POST'])
def google_login_handler():
    return gconnect.connect_google_user(flask.request.data)

@app.route('/logout')
def logout_handler():
    return logout.logout()

@decorators.check_signed_in
@app.route('/addcatalog', methods=['GET', 'POST'])
def add_catalog_handler():
    username = flask.session.get('username')
    if flask.request.method == 'GET':
        return flask.render_template('addcatalog.html', username=username, catalog=None)
    elif flask.request.method == 'POST':
        return catalog.add_new_catalog(flask.request.form, flask.request.files)

class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code
    return response