import logging
import flask
from werkzeug.exceptions import BadRequest, Unauthorized

import models
import login
import uploadfile
from itemcatalog import app

@app.route('/', methods=['GET'])
def main_page_handler():
    user = models.get_current_user()
    catalogs = models.get_catalogs()
    return flask.render_template('index.html', user=user, catalogs=catalogs)

@app.route('/catalog/<catalog_id>', methods=['GET'])
def catalog_view_handler(catalog_id):
    user = models.get_current_user()
    catalog_id = int(catalog_id)
    catalog = models.get_catalog_by_id(catalog_id)
    if not catalog:
        raise BadRequest('Could not find catalog with id %d!' % catalog_id)
    categories = models.get_categories(catalog_id)
    return flask.render_template('catalog.html', user=user, catalog=catalog, categories=categories)


@app.route('/addcatalog', methods=['GET', 'POST'])
@login.check_logged_in
def add_catalog_handler():
    user = models.get_current_user()

    if flask.request.method == 'GET':
        return flask.render_template('addcatalog.html', user=user, catalog=None)

    elif flask.request.method == 'POST':
        try:
            cover_picture_obj = flask.request.files.get('cover_picture')
            cover_picture_url = uploadfile.save_file(cover_picture_obj)

            new_catalog = models.Catalog(name=flask.request.form.get('name'),
                                         description=flask.request.form.get('description'),
                                         cover_picture=cover_picture_url,
                                         owner=user.key)
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
    user = models.get_current_user()
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d!' % catalog_id)

    if not catalog_entity.user_can_edit(user):
        raise Unauthorized

    if flask.request.method == 'GET':
        return flask.render_template('editcatalog.html', user=user, catalog=catalog_entity)

    elif flask.request.method == 'POST':
        try:
            cover_picture_obj = flask.request.files.get('cover_picture')
            cover_picture_url = uploadfile.save_file(cover_picture_obj)
            # TODO: delete old picture
            catalog_entity.cover_picture = uploadfile.save_file(cover_picture_url)
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
    catalog_id = int(catalog_id)
    catalog_entity = models.get_catalog_by_id(catalog_id)
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d!' % catalog_id)

    if not catalog_entity.user_can_edit(models.get_current_user()):
        raise Unauthorized

    models.delete_catalog(catalog_id)

    return flask.redirect('/')
