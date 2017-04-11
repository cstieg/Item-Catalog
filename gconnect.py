import logging
import flask
import json
import httplib2
import werkzeug
import oauth2client.client
from google.appengine.api import urlfetch

from itemcatalog import app
from helper import http_response
import login

@app.route('/gconnect', methods=['POST'])
def gconnect():
    try:
        credentials = getGoogleCredentials()
    except oauth2client.client.FlowExchangeError:
        return http_response('Failed to upgrade the authorization code.', 401)

    try:
        data = getGoogleUserInfo(credentials)
    except:
        return http_response('Error retrieving user info!', response.status_code)


    flask.session['provider'] = 'google'
    flask.session['username'] = data['name']
    flask.session['picture'] = data['picture']
    flask.session['email'] = data['email']

    # Create user if not in database
    new_user = login.create_user(data['email'], data['name'], 'google', data['picture'])
    if not new_user:
        return http_response('Could not create new user!', 401)

    return http_response('Success!', 200)

def getGoogleCredentials():
    code = flask.request.data

    # Upgrade the authorization code into a credentials object
    oauth_flow = oauth2client.client.flow_from_clientsecrets('client_secrets.json', scope='')
    oauth_flow.redirect_uri = 'postmessage'
    credentials = oauth_flow.step2_exchange(code)

    # Store the access token in the session for later use
    flask.session['access_token'] = credentials.access_token
    return credentials


def getGoogleUserInfo(credentials):
    access_token = credentials.access_token

    # Get user info
    response = urlfetch.fetch(
        url='https://www.googleapis.com/oauth2/v2/userinfo?access_token=%s' % access_token,
        method=urlfetch.GET)

    if response.status_code >= 400:
        raise werkzeug.exceptions.BadRequest('Cannot access user information!')

    return json.loads(response.content)

def gdisconnect():
    access_token = flask.session.get('access_token')
    response = urlfetch.fetch(
        url='https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token,
        method=urlfetch.GET)

    if response.status_code >= 400:
        raise werkzeug.exceptions.BadRequest('Failed to revoke token for user')

