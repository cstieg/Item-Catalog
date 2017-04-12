import logging
import flask
import decorators
import logout
import gconnect
import catalog
from itemcatalog import app

@app.route('/')
def main_page_handler():
    username = flask.session.get('username')
    return flask.render_template('index.html', username=username)

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
