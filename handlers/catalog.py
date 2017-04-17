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
    catalog = models.get_catalog_by_id(catalog_id)
    if not catalog:
        raise BadRequest('Could not find catalog with id %d!' % catalog_id)
    categories = models.get_categories(catalog_id)
    return flask.render_template('catalog.html', username=username, catalog=catalog, categories=categories)


@app.route('/addcatalog', methods=['GET', 'POST'])
@login.check_logged_in
def add_catalog_handler():
    username = flask.session.get('username')

    if flask.request.method == 'GET':
        return flask.render_template('addcatalog.html', username=username, catalog=None)

    elif flask.request.method == 'POST':
        try:
            cover_picture_obj = flask.request.files.get('cover_picture')
            cover_picture_url = uploadfile.save_file(cover_picture_obj)
            owner = login.get_current_user()

            new_catalog = models.Catalog(name=flask.request.form.get('name'),
                                         description=flask.request.form.get('description'),
                                         cover_picture=cover_picture_url,
                                         owner=owner.key)
            new_catalog.put()
            models.wait_for(new_catalog)
            return flask.redirect('/catalog/%d' % new_catalog.key.id())
        except IOError:
            return ('Failed to add new catalog', 401)

@app.route('/editcatalog/<catalog_id>', methods=['GET', 'POST'])
@login.check_logged_in
def edit_catalog_handler(catalog_id):
    catalog_id = int(catalog_id)
    catalog_entity = models.get_catalog_by_id(catalog_id)
    username = flask.session.get('username')
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d!' % catalog_id)

    if flask.request.method == 'GET':
        return flask.render_template('editcatalog.html', username=username, catalog=catalog_entity)

    elif flask.request.method == 'POST':
        try:
            cover_picture_obj = flask.request.files.get('cover_picture')
            # TODO: delete old picture
            catalog_entity.cover_picture = uploadfile.save_file(cover_picture_obj)
            catalog_entity.name = flask.request.form.get('name')
            catalog_entity.description = flask.request.form.get('description')

            catalog_entity.put()
            models.wait_for(catalog_entity)
            return flask.redirect('/catalog/%d' % catalog_entity.key.id())
        except IOError:
            return ('Failed to edit catalog', 401)

@app.route('/deletecatalog/<catalog_id>', methods=['POST'])
@login.check_logged_in
def delete_catalog_handler(catalog_id):
    username = flask.session.get('username')
    catalog_id = int(catalog_id)
    catalog_entity = models.get_catalog_by_id(catalog_id)
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d!' % catalog_id)
    models.delete_catalog(catalog_id)
    models.wait_for(catalog_entity)
    return flask.redirect('/')
