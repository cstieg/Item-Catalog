import flask
from google.appengine.ext import ndb
from werkzeug.exceptions import BadRequest

import models
import login
from itemcatalog import app

@login.check_logged_in
@app.route('/catalog/<catalog_id>/addcategory', methods=['GET', 'POST'])
def add_category_handler(catalog_id):
    username = flask.session.get('username')
    catalog_id = int(catalog_id)
    catalog_entity = models.get_catalog_by_id(catalog_id)
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d' % catalog_id)

    if flask.request.method == 'GET':
        return flask.render_template('addcategory.html', username=username, catalog=catalog_entity, category=None)

    elif flask.request.method == 'POST':
        new_category = models.Category(name=flask.request.form.get('name'),
                                     description=flask.request.form.get('description'),
                                     catalog=catalog_entity.key)
        new_category.put()
        models.wait_for(new_category)
        return flask.redirect('/catalog/%d' % catalog_entity.key.id())

@login.check_logged_in
@app.route('/catalog/<catalog_id>/editcategory/<category_id>', methods=['GET', 'POST'])
def edit_category_handler(catalog_id, category_id):
    username = flask.session.get('username')
    catalog_id = int(catalog_id)
    catalog_entity = models.get_catalog_by_id(catalog_id)
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d' % catalog_id)

    category_id = int(category_id)
    category_entity = models.get_category_by_id(catalog_id, category_id)
    if not (category_entity):
        raise BadRequest('Could not find category with id %d!' % category_id)

    if flask.request.method == 'GET':
        return flask.render_template('editcategory.html', username=username, catalog=catalog_entity, category=category_entity)

    elif flask.request.method == 'POST':
        category_entity.name = flask.request.form.get('name')
        category_entity.description = flask.request.form.get('description')
        category_entity.put()
        models.wait_for(category_entity)
        return flask.redirect('/catalog/%d' % catalog_entity.key.id())

@login.check_logged_in
@app.route('/catalog/<catalog_id>/deletecategory/<category_id>', methods=['POST'])
def delete_category_handler(catalog_id, category_id):
    username = flask.session.get('username')
    catalog_id = int(catalog_id)
    catalog_entity = models.get_catalog_by_id(catalog_id)
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d' % catalog_id)

    category_id = int(category_id)
    category_entity = models.get_category_by_id(catalog_id, category_id)
    if not (category_entity):
        raise BadRequest('Could not find category with id %d!' % category_id)

    models.delete_category(catalog_id, category_id)
    models.wait_for(category_entity)
    return flask.redirect('/catalog/%d' % catalog_entity.key.id())
