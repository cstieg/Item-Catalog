import logging
import flask
import json
import httplib2
import werkzeug
import oauth2client.client
from google.appengine.api import urlfetch

from helper import http_response, success_response
from models import user_login

def connect_google_user(code):
    try:
        credentials = get_google_credentials(code)
    except oauth2client.client.FlowExchangeError:
        return http_response('Failed to upgrade the authorization code.', 401)

    try:
        data = get_google_user_info(credentials.access_token)
    except:
        return http_response('Error retrieving user info!', response.status_code)

    flask.session['provider'] = 'google'
    flask.session['username'] = data['name']
    flask.session['picture'] = data['picture']
    flask.session['email'] = data['email']

    logging.info(data['email'])
    # Create user if not in database
    new_user = user_login.create_user(data['email'], data['name'], 'google', data['picture'])
    if not new_user:
        return http_response('Could not create new user!', 401)

    return success_response()

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
        raise werkzeug.exceptions.BadRequest('Cannot access user information!')

    return json.loads(response.content)

def disconnect_google_user():
    access_token = flask.session.get('access_token')
    response = urlfetch.fetch(
        url='https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token,
        method=urlfetch.GET)
    logging.info(response.status_code)

    if response.status_code >= 400:
        raise werkzeug.exceptions.BadRequest('Failed to revoke token for user')


