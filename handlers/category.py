"""Handlers for category"""

import flask
from werkzeug.exceptions import BadRequest, Unauthorized
from json import dumps

from flaskapp import app
import models
from decorators import check_logged_in


@app.route('/catalog/<catalog_id>/addcategory', methods=['GET', 'POST'])
@check_logged_in
def add_category_handler(catalog_id):
    """Adds a category to a catalog
    Parameters:
    - catalog_id: integer id of catalog to which category belongs
    
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
        # Render add category form
        return flask.render_template('addcategory.html',
                                     user=user,
                                     catalog=catalog_entity,
                                     category=None)

    elif flask.request.method == 'POST':
        # Handle new category submission from form
        new_category = models.add_category(flask.request.form.get('name'),
                                           flask.request.form.get('description'),
                                           catalog_entity.catalog_id)

        return flask.redirect('/catalog/%d' % catalog_entity.catalog_id)

@app.route('/catalog/<catalog_id>/editcategory/<category_id>', methods=['GET', 'POST'])
@check_logged_in
def edit_category_handler(catalog_id, category_id):
    """Edits a category in a catalog
    Parameters:
    - catalog_id: integer id of catalog to which category belongs
    - category_id: integer id of category to edit
    
    Returns:
    - HTTP response
    """
    user = models.get_current_user()
    catalog_id = int(catalog_id)
    catalog_entity = models.get_catalog_by_id(catalog_id)
    category_id = int(category_id)
    category_entity = models.get_category_by_id(catalog_id, category_id)

    # Check parameters
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d' % catalog_id)
    if not (category_entity):
        raise BadRequest('Could not find category with id %d!' % category_id)
    if not models.user_can_edit(user.username, catalog_id):
        raise Unauthorized

    if flask.request.method == 'GET':
        # Render edit category form
        return flask.render_template('editcategory.html',
                                     user=user,
                                     catalog=catalog_entity,
                                     category=category_entity)

    elif flask.request.method == 'POST':
        # Handle category edit from form
        models.edit_category(category_id,
                             catalog_id,
                             flask.request.form.get('name'),
                             flask.request.form.get('description'))

        return flask.redirect('/catalog/%d' % catalog_entity.catalog_id)

@app.route('/catalog/<catalog_id>/deletecategory/<category_id>', methods=['POST'])
@check_logged_in
def delete_category_handler(catalog_id, category_id):
    """Deletes a category in a catalog
    Parameters:
    - catalog_id: integer id of catalog to which category belongs
    - category_id: integer id of category to delete
    
    Returns:
    - HTTP response redirecting to catalog page
    """
    catalog_id = int(catalog_id)
    catalog_entity = models.get_catalog_by_id(catalog_id)
    category_id = int(category_id)
    category_entity = models.get_category_by_id(catalog_id, category_id)
    user = models.get_current_user()

    # Check parameters
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d' % catalog_id)
    if not (category_entity):
        raise BadRequest('Could not find category with id %d!' % category_id)
    if not models.user_can_edit(user.username, catalog_id):
        raise Unauthorized

    models.delete_category(catalog_id, category_id)

    return flask.redirect('/catalog/%d' % catalog_entity.catalog_id)

@app.route('/catalog/<catalog_id>/category/<category_id>/json', methods=['GET'])
def category_json_endpoint(catalog_id, category_id):
    """Returns category entity in JSON form
    Parameters:
    - catalog_id: integer id of catalog to which category belongs
    - category_id: integer id of category
    """
    return dumps(models.get_category_dict(int(catalog_id), int(category_id)), default=models.json_serial)
