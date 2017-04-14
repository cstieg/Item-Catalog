import logging
import flask
import json

def success_response():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

def success():
    return json.dumps({'success':True}), 200, {'ContentType':'application/json'}