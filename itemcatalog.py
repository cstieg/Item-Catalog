import logging
import os
import flask
import random
import string

app = flask.Flask(__name__)
app.secret_key = 'ZAwsBF5SZD6#QzwRnDvakmJ5xp4d7XqRaxX#^V!T'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

GCLOUD_STORAGE_BUCKET = 'itemcatalog-163806.appspot.com'
PROJECT_ID = 'itemcatalog-163806'

from handlers.handler_list import *
