"""Logout handler"""

import logging
import flask

from itemcatalog import app
import models

@app.route('/logout', methods=['POST'])
def logout_handler():
    """Logs a user out by clearing the session"""
    user = models.get_current_user()
    if not user:
        logging.info('Already logged out!')
        return flask.redirect(flask.url_for('main_page_handler'))

    # Reset the user's session.
    flask.session.clear()

    flask.flash('Logged out!')
    return flask.redirect(flask.url_for('main_page_handler'))
