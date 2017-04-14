import flask
import gconnect
from werkzeug.exceptions import BadRequest
from itemcatalog import app

@app.route('/logout', methods=['GET'])
def logout_handler():
    username = flask.session.get('username')
    if not username:
        logging.info('Already logged out!')
        return flask.redirect(flask.url_for('main_page_handler'))

    if flask.session.get('provider') == 'google':
        try:
            gconnect.disconnect_google_user()
        except BadRequest:
            flask.flash('Failed to revoke Google tokens for user!')

    # Reset the user's session.
    flask.session.clear()

    flask.flash('Logged out!')
    return flask.redirect(flask.url_for('main_page_handler'))
