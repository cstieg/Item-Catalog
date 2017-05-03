"""Handlers for catalog items"""

import flask
from werkzeug.exceptions import BadRequest
from json import dumps

from itemcatalog import app
import models
import login
import uploadfile

@app.route('/catalog/<catalog_id>/additem', methods=['GET', 'POST'])
@login.check_logged_in
def add_item_handler(catalog_id):
    """Adds an item to a catalog
    Parameters:
    - catalog_id: integer id of catalog to which item belongs
    
    Returns:
    - HTTP response
    """
    user = models.get_current_user()
    catalog_id = int(catalog_id)
    catalog_entity = models.get_catalog_by_id(catalog_id)

    # Check parameters
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d' % catalog_id)
    if not models.user_can_edit(user.username, catalog_id):
        raise Unauthorized

    if flask.request.method == 'GET':
        # Render add item form
        # Category_id may be passed in if adding item from category edit page
        category_id = flask.request.args.get('category_id')
        if category_id:
            category_id = int(category_id)

        categories = models.get_categories(catalog_id)
        return flask.render_template('additem.html',
                                     user=user,
                                     catalog=catalog_entity,
                                     category_id=category_id,
                                     categories=categories,
                                     item=None)

    elif flask.request.method == 'POST':
        # Handle new item submission from form
        picture_obj = flask.request.files.get('picture')
        picture_url = uploadfile.save_file(picture_obj)

        try:
            price = float(flask.request.form.get('price'))
        except:
            price = 0.00

        category_id = flask.request.form.get('category_id')
        if category_id:
            category_id = int(category_id)
        new_item = models.add_item(flask.request.form.get('name'),
                                   flask.request.form.get('description'),
                                   price,
                                   picture_url,
                                   user.username,
                                   catalog_id,
                                   category_id)

        return flask.redirect('/catalog/%d' % catalog_id)

@app.route('/catalog/<catalog_id>/edititem/<item_id>', methods=['GET', 'POST'])
@login.check_logged_in
def edit_item_handler(catalog_id, item_id):
    """Edits an item in a catalog
    Parameters:
    - catalog_id: integer id of catalog to which item belongs
    - item_id: integer id of item to edit
    
    Returns:
    - HTTP response
    """
    user = models.get_current_user()
    catalog_id = int(catalog_id)
    catalog_entity = models.Catalog.get_by_id(catalog_id)
    item_id = int(item_id)
    item_entity = models.get_item_by_id(catalog_id, item_id)

    # Check parameters
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d' % catalog_id)
    if not (item_entity):
        raise BadRequest('Could not find item with id %d!' % item_id)
    if not models.user_can_edit(user.username, catalog_id):
        raise Unauthorized

    if flask.request.method == 'GET':
        # Render edit item form
        categories = models.get_categories(catalog_id)
        return flask.render_template('edititem.html',
                                     user=user,
                                     catalog=catalog_entity,
                                     categories=categories,
                                     category_id=item_entity.category,
                                     item=item_entity)

    elif flask.request.method == 'POST':
        # Handle item edit from form
        picture_obj = flask.request.files.get('picture')
        picture_url = uploadfile.save_file(picture_obj)

        try:
            price = float(flask.request.form.get('price'))
        except:
            price = 0.00

        category_id = flask.request.form.get('category_id')
        if category_id:
            category_id = int(category_id)

        # Update entity
        models.edit_item(item_id,
                         flask.request.form.get('name'),
                         flask.request.form.get('description'),
                         price,
                         picture_url,
                         catalog_id,
                         category_id)

        return flask.redirect('/catalog/%d' % catalog_id)

@app.route('/catalog/<catalog_id>/deleteitem/<item_id>', methods=['POST'])
@login.check_logged_in
def delete_item_handler(catalog_id, item_id):
    """Deletes an item in a catalog
    Parameters:
    - catalog_id: integer id of catalog to which item belongs
    - item_id: integer id of item to delete
    
    Returns:
    - HTTP response redirecting to catalog page
    """
    catalog_id = int(catalog_id)
    catalog_entity = models.get_catalog_by_id(catalog_id)
    item_id = int(item_id)
    item_entity = models.get_item_by_id(catalog_id, item_id)
    user = models.get_current_user()

    # Check parameters
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d' % catalog_id)
    if not (item_entity):
        raise BadRequest('Could not find item with id %d!' % item_id)
    if not models.user_can_edit(user.username, catalog_id):
        raise Unauthorized

    models.delete_item(catalog_id, item_id)
    return flask.redirect('/catalog/%d' % catalog_entity.catalog_id)

@app.route('/catalog/<catalog_id>/item/<item_id>/json', methods=['GET'])
def item_json_endpoint(catalog_id, item_id):
    """Returns item entity in JSON form
    Parameters:
    - catalog_id: integer id of catalog to which item belongs
    - item_id: integer id of item
    """
    return dumps(models.get_item_dict(int(catalog_id), int(item_id)), default=models.json_serial)
