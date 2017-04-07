import flask

def signup():
    if flask.request.method == 'GET':
        return flask.render_template('signup.html', user='')