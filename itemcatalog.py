"""
Item catalog that allows users to login in through Google and create catalogs
of items organized by categories to be viewable by the public.

Written using the Flask framework and the Google App Engine on the Google Cloud Platform.

This is the main entry point that sets up the Flask application.
"""

import os
import flask
import logging


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')




from flaskapp import app

# After creating the Flask app, import the handlers which reference it
from handlers import *

if __name__ == "__main__":
    app.run()