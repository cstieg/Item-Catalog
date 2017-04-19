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
    if not catalog_entity.user_can_edit(user):
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

        new_item = models.Item(name=flask.request.form.get('name'),
                               description=flask.request.form.get('description'),
                               price=price,
                               picture=picture_url,
                               owner=user.key,
                               catalog=catalog_entity.key)

        # Allow possibility of putting items without category
        category_id = flask.request.form.get('category_id')
        if category_id:
            category_id = int(category_id)
        category_entity = models.get_category_by_id(catalog_id, category_id)
        if category_entity:
            new_item.category = category_entity.key

        new_item.put()
        models.wait_for(new_item)
        return flask.redirect('/catalog/%d' % catalog_entity.key.id())

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
    if not catalog_entity.user_can_edit(user):
        raise Unauthorized

    if flask.request.method == 'GET':
        # Render edit item form
        categories = models.get_categories(catalog_id)
        return flask.render_template('edititem.html',
                                     user=user,
                                     catalog=catalog_entity,
                                     categories=categories,
                                     category_id=item_entity.category.id(),
                                     item=item_entity)

    elif flask.request.method == 'POST':
        # Handle item edit from form
        picture_obj = flask.request.files.get('picture')
        picture_url = uploadfile.save_file(picture_obj)

        try:
            price = float(flask.request.form.get('price'))
        except:
            price = 0.00

        # Update entity
        item_entity.name = flask.request.form.get('name')
        item_entity.description = flask.request.form.get('description')
        item_entity.price = price
        item_entity.picture = picture_url

        # Allow possibility of item without category
        category_id = flask.request.form.get('category_id')
        if category_id:
            category_id = int(category_id)
        category_entity = models.get_category_by_id(catalog_id, category_id)
        if category_entity:
            item_entity.category = category_entity.key

        item_entity.put()
        models.wait_for(item_entity)
        return flask.redirect('/catalog/%d' % catalog_entity.key.id())

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

    # Check parameters
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d' % catalog_id)
    if not (item_entity):
        raise BadRequest('Could not find item with id %d!' % item_id)
    if not catalog_entity.user_can_edit(models.get_current_user()):
        raise Unauthorized

    models.delete_item(catalog_id, item_id)
    return flask.redirect('/catalog/%d' % catalog_entity.key.id())

@app.route('/catalog/<catalog_id>/item/<item_id>/json', methods=['GET'])
def item_json_endpoint(catalog_id, item_id):
    """Returns item entity in JSON form
    Parameters:
    - catalog_id: integer id of catalog to which item belongs
    - item_id: integer id of item
    """
    return dumps(models.get_item_dict(int(catalog_id), int(item_id)), default=models.json_serial)
