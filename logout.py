import flask
import logging
import gconnect

def logout():
    username = flask.session.get('username')
    logging.info(username)
    if not username:
        logging.info('Already logged out!')
        return flask.redirect(flask.url_for('main_page_handler'))

    if flask.session.get('provider') == 'google':
        try:
            gconnect.gdisconnect()
        except:
            return ('Failed to revoke Google tokens for user!', 401)

    # Reset the user's session.
    flask.session.clear()

    return flask.render_template('index.html', message='Logged out!')
