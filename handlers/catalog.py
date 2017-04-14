import logging
import flask
from werkzeug.exceptions import BadRequest

import models
import login
import uploadfile
from itemcatalog import app

@app.route('/', methods=['GET'])
def main_page_handler():
    username = flask.session.get('username')
    catalogs = models.get_catalogs()
    return flask.render_template('index.html', username=username, catalogs=catalogs)

@app.route('/catalog/<catalog_id>', methods=['GET'])
def catalog_view_handler(catalog_id):
    username = flask.session.get('username')
    catalog_id = int(catalog_id)
    catalog = models.get_catalogs(catalog_id)
    if not catalog:
        flask.flash('Could not find catalog with id %d!' % catalog_id)
    categories = models.get_categories(catalog_id)
    return flask.render_template('catalog.html', username=username, catalog=catalog, categories=categories)

@login.check_logged_in
@app.route('/addcatalog', methods=['GET', 'POST'])
def add_catalog_handler():
    username = flask.session.get('username')
    if flask.request.method == 'GET':
        return flask.render_template('addcatalog.html', username=username, catalog=None)
    elif flask.request.method == 'POST':
        try:
            cover_picture_obj = flask.request.files.get('cover_picture')
            cover_picture_url = uploadfile.save_file(cover_picture_obj)
            owner = login.get_current_user()
            owner_key = owner.key
            name = flask.request.form.get('name')
            description = flask.request.form.get('description')

            new_catalog = models.Catalog(name=name,
                                         description=description,
                                         cover_picture=cover_picture_url,
                                         owner=owner_key)
            new_catalog.put()
            return flask.redirect('/catalog/%d' % new_catalog.key.id())
        except IOError:
            return ('Failed to add new catalog', 401)

@login.check_logged_in
@app.route('/editcatalog/<catalog_id>', methods=['GET', 'POST'])
def edit_catalog_handler(catalog_id):
    catalog_id = int(catalog_id)
    catalog = models.get_catalogs(catalog_id)
    username = flask.session.get('username')
    if not catalog:
        flask.flash('Could not find catalog with id %d!' % catalog_id)
        raise BadRequest

    if flask.request.method == 'GET':
        return flask.render_template('editcatalog.html', username=username, catalog=catalog)

    elif flask.request.method == 'POST':
        try:

            cover_picture_obj = flask.request.files.get('cover_picture')
            # TODO: delete old picture
            catalog.cover_picture = uploadfile.save_file(cover_picture_obj)
            catalog.name = flask.request.form.get('name')
            catalog.description = flask.request.form.get('description')

            catalog.put()
            return flask.redirect('/catalog/%d' % catalog.key.id())
        except IOError:
            return ('Failed to edit catalog', 401)

@login.check_logged_in
@app.route('/deletecatalog/<catalog_id>', methods=['POST'])
def delete_catalog_handler(catalog_id):
    username = flask.session.get('username')
    catalog_id = int(catalog_id)
    catalog = models.get_catalogs(catalog_id)
    if not catalog:
        flask.flash('Could not find catalog with id %d!' % catalog_id)
        raise BadRequest
    models.delete_catalog(catalog_id)
    return flask.redirect('/')
