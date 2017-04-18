import logging
import flask
import gconnect
import models
from werkzeug.exceptions import BadRequest
from itemcatalog import app

@app.route('/logout', methods=['POST'])
def logout_handler():
    user = models.get_current_user()
    if not user:
        logging.info('Already logged out!')
        return flask.redirect(flask.url_for('main_page_handler'))

    # Reset the user's session.
    flask.session.clear()

    flask.flash('Logged out!')
    return flask.redirect(flask.url_for('main_page_handler'))
