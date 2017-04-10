import logging
import flask

def http_response(message, response_code):
    if response_code >= 400:
        logging.error(message)
    else:
        logging.info(message)
    response = flask.make_response(message, response_code)
    response.headers['Content-Type'] = 'application/json'
    return response
