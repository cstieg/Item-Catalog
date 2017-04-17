import logging
import flask
import json
import oauth2client.client
from google.appengine.api import urlfetch
from werkzeug.exceptions import HTTPException, BadRequest, Unauthorized, InternalServerError

import responses
from models import user_login
from itemcatalog import app

@app.route('/gconnect', methods=['POST'])
def google_login_handler():

    code = flask.request.data
    try:
        credentials = get_google_credentials(code)
    except oauth2client.client.FlowExchangeError:
        raise Unauthorized('Failed to upgrade the Google authorization code.')

    try:
        data = get_google_user_info(credentials.access_token)
    except:
        raise HTTPException('Error retrieving user info from Google!', response)

    flask.session['provider'] = 'google'
    flask.session['username'] = data['name']
    flask.session['picture'] = data['picture']
    flask.session['email'] = data['email']

    logging.info(data['email'])
    # Create user if not in database
    new_user = user_login.create_user(data['email'], data['name'], 'google', data['picture'])
    if not new_user:
        raise InternalServerError('Could not create new user!')

    return responses.success()

def get_google_credentials(code):
    # Upgrade the authorization code into a credentials object
    oauth_flow = oauth2client.client.flow_from_clientsecrets('client_secrets.json', scope='')
    oauth_flow.redirect_uri = 'postmessage'
    credentials = oauth_flow.step2_exchange(code)

    # Store the access token in the session for later use
    flask.session['access_token'] = credentials.access_token
    return credentials

def get_google_user_info(access_token):
    # Get user info
    response = urlfetch.fetch(
        url='https://www.googleapis.com/oauth2/v2/userinfo?access_token=%s' % access_token,
        method=urlfetch.GET)

    if response.status_code >= 400:
        raise HTTPException('Cannot access user information from Google!', response)

    return json.loads(response.content)

def disconnect_google_user():
    access_token = flask.session.get('access_token')
    response = urlfetch.fetch(
        url='https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token,
        method=urlfetch.GET)
    logging.info(response.status_code)

    if response.status_code >= 400:
        raise BadRequest('Failed to revoke token for user')


