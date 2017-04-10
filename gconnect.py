import logging
import flask
import json
import httplib2
from google.appengine.api import urlfetch
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError

from itemcatalog import app
from helper import http_response
import login

@app.route('/gconnect', methods=['POST'])
def gconnect():
#     if flask.request.args.get('state') != flask.session.get('state'):
#         response = flask.make_response(json.dumps('Invalid state parameters'), 401)
#         response.headers['Content-Type'] = 'application/json'
#         return response
    credentials = getGoogleCredentials()

    # check to see whether error response was returned rather than credentials
    if isinstance(credentials, flask.Response):
        return credentials

    # check to see whether error response was returned rather than data
    data = getGoogleUserInfo(credentials)

    # check to see whether error response was returned rather than data
    if isinstance(data, flask.Response):
        return data

    flask.session['provider'] = 'google'
    flask.session['username'] = data['name']
    flask.session['picture'] = data['picture']
    flask.session['email'] = data['email']

    # Create user if not in database
    new_user = login.create_user(data['email'], data['name'], 'google', data['picture'])
    if not new_user:
        return http_response('Could not create new user!', 401)

    return ('Success', 200)

def getGoogleCredentials():
    code = flask.request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        return http_response('Failed to upgrade the authorization code.', 401)

    # Store the access token in the session for later use
    flask.session['credentials'] = credentials.to_json()
    return credentials


def getGoogleUserInfo(credentials):
    access_token = credentials.access_token

    # Get user info
    response = urlfetch.fetch(
        url='https://www.googleapis.com/oauth2/v2/userinfo?access_token=%s' % access_token,
        method=urlfetch.GET)

    if response.status_code >= 400:
        return http_response('Error retrieving user info!', response.status_code)

    return json.loads(response.content)


@app.route("/disconnect")
def gdisconnect():
    # Only disconnect a connected user.
    credentials = flask.session.get('credentials')
    if credentials is None:
        response = flask.make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session.
        del flask.session['credentials']
        del flask.session['gplus_id']
        del flask.session['username']
        del flask.session['email']
        del flask.session['picture']

        response = flask.make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = flask.make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
