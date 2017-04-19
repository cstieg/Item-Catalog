"""
Item catalog that allows users to login in through Google and create catalogs
of items organized by categories to be viewable by the public.

Written using the Flask framework and the Google App Engine on the Google Cloud Platform.

This is the main entry point that sets up the Flask application.
"""

import os
import flask

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')

# Update these constants with ids supplied by Google App Engine
PROJECT_ID = 'itemcatalog-163806'
GCLOUD_STORAGE_BUCKET = 'itemcatalog-163806.appspot.com'


app = flask.Flask(__name__)
app.secret_key = 'ZAwsBF5SZD6#QzwRnDvakmJ5xp4d7XqRaxX#^V!T'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DEBUG'] = False
app.config['TESTING'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True

# After creating the Flask app, import the handlers which reference it
from handlers import *
