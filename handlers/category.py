import flask
from google.appengine.ext import ndb
from werkzeug.exceptions import BadRequest

import models
import login
from itemcatalog import app

@login.check_logged_in
@app.route('/catalog/<catalog_id>/addcategory', methods=['GET', 'POST'])
def add_category_handler(catalog_id):
    catalog_id = int(catalog_id)
    catalog = models.get_catalogs(catalog_id)
    username = flask.session.get('username')
    if not catalog:
        flask.flash('Could not find catalog with id %d!' % catalog_id)
        raise BadRequest('Could not find catalog with id %d' % catalog_id)

    if flask.request.method == 'GET':
        return flask.render_template('addcategory.html', username=username, catalog=catalog, category=None)

    elif flask.request.method == 'POST':
        try:
            name = flask.request.form.get('name')
            description = flask.request.form.get('description')
            new_category = models.Category(name=name,
                                         description=description,
                                         catalog=catalog.key)
            new_category.put()
            return flask.redirect('/catalog/%d' % catalog.key.id())
        except IOError:
            return ('Failed to add new catalog', 401)