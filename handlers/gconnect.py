"""Login through Google OAuth2"""

import flask
import json
import oauth2client.client
from google.appengine.api import urlfetch
from werkzeug.exceptions import BadRequest, Unauthorized, InternalServerError

from itemcatalog import app
import responses
from models import user_login

@app.route('/gconnect', methods=['POST'])
def google_login_handler():
    """Callback from clientside to exchange Google authorization code for credentials"""
    code = flask.request.data
    try:
        credentials = get_google_credentials(code)
    except oauth2client.client.FlowExchangeError:
        raise Unauthorized('Failed to upgrade the Google authorization code.')

    data = get_google_user_info(credentials.access_token)

    # Store user info in session
    flask.session['provider'] = 'google'
    flask.session['username'] = data['name']
    flask.session['picture'] = data['picture']
    flask.session['email'] = data['email']

    # Create user if not in database
    new_user = user_login.create_user(data['email'], data['name'], 'google', data['picture'])
    if not new_user:
        raise InternalServerError('Could not create new user!')

    return responses.success()

def get_google_credentials(code):
    """Upgrades the authorization code into a credentials object"""
    oauth_flow = oauth2client.client.flow_from_clientsecrets('client_secrets.json', scope='')
    oauth_flow.redirect_uri = 'postmessage'
    credentials = oauth_flow.step2_exchange(code)

    # Store the access token in the session for later use
    flask.session['access_token'] = credentials.access_token
    return credentials

def get_google_user_info(access_token):
    """Gets Google user info from access token"""
    response = urlfetch.fetch(
        url='https://www.googleapis.com/oauth2/v2/userinfo?access_token=%s' % access_token,
        method=urlfetch.GET)

    if response.status_code >= 400:
        raise InternalServerError('Cannot access user information from Google!', response)

    return json.loads(response.content)
