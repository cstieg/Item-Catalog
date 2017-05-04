"""Handers for catalogs"""
import logging
import flask
from werkzeug.exceptions import BadRequest, Unauthorized
from json import dumps

from flaskapp import app
from decorators import check_logged_in
import models
import uploadfile

@app.route('/', methods=['GET'])
def main_page_handler():
    """Renders the main page, a list of the available catalogs"""
    user = models.get_current_user()
    catalogs = models.get_catalogs()
    logging.info(user)
    return flask.render_template('index.html', user=user, catalogs=catalogs)

@app.route('/catalog/<catalog_id>', methods=['GET'])
def catalog_view_handler(catalog_id):
    """Renders a catalog page
     Parameters:
    - catalog_id: integer id of catalog to be rendered

    Returns:
    - HTTP response
    """
    user = models.get_current_user()
    catalog_id = int(catalog_id)
    catalog = models.get_catalog_by_id(catalog_id)
    if not catalog:
        raise BadRequest('Could not find catalog with id %d!' % catalog_id)
    categories = models.get_categories(catalog_id)
    return flask.render_template('catalog.html', user=user, catalog=catalog, categories=categories)

@app.route('/addcatalog', methods=['GET', 'POST'])
@check_logged_in
def add_catalog_handler():
    """Adds a catalog
    Returns:
    - HTTP response
    """
    user = models.get_current_user()
    print "user: "
    print user
    if flask.request.method == 'GET':
        # Render add catalog form
        return flask.render_template('addcatalog.html', user=user, catalog=None)

    elif flask.request.method == 'POST':
        # Handle new catalog submission from form
        try:
            cover_picture_obj = flask.request.files.get('cover_picture')
            cover_picture_url = uploadfile.save_file(cover_picture_obj)
            new_catalog = models.add_catalog(flask.request.form.get('name'),
                                             flask.request.form.get('description'),
                                             cover_picture_url,
                                             user.username)

            return flask.redirect('/catalog/%d' % new_catalog.catalog_id)
        except IOError:
            return ('Failed to add new catalog', 401)

@app.route('/editcatalog/<catalog_id>', methods=['GET', 'POST'])
@check_logged_in
def edit_catalog_handler(catalog_id):
    """Edits a catalog
    Parameters:
    - catalog_id: integer id of catalog to edit

    Returns:
    - HTTP response
    """
    catalog_id = int(catalog_id)
    catalog_entity = models.get_catalog_by_id(catalog_id)
    user = models.get_current_user()

    # Check parameters
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d!' % catalog_id)
    if not models.user_can_edit(user.username, catalog_id):
        raise Unauthorized

    if flask.request.method == 'GET':
        # Render edit catalog form
        return flask.render_template('editcatalog.html', user=user, catalog=catalog_entity)

    elif flask.request.method == 'POST':
        # Handle catalog edit from form
        try:
            cover_picture_obj = flask.request.files.get('cover_picture')
            cover_picture_url = uploadfile.save_file(cover_picture_obj)
            # TODO: delete old picture
            models.edit_catalog(catalog_id,
                                flask.request.form.get('name'),
                                flask.request.form.get('description'),
                                uploadfile.save_file(cover_picture_url),
                                user.username)

            return flask.redirect('/catalog/%d' % catalog_entity.catalog_id)
        except IOError:
            return ('Failed to edit catalog', 401)

@app.route('/deletecatalog/<catalog_id>', methods=['POST'])
@check_logged_in
def delete_catalog_handler(catalog_id):
    """Deletes a catalog
    Parameters:
    - catalog_id: integer id of catalog to delete

    Returns:
    - HTTP response redirecting to index
    """
    catalog_id = int(catalog_id)
    catalog_entity = models.get_catalog_by_id(catalog_id)
    user = models.get_current_user()

    # Check parameters
    if not catalog_entity:
        raise BadRequest('Could not find catalog with id %d!' % catalog_id)
    if not models.user_can_edit(user.username, catalog_id):
        raise Unauthorized

    models.delete_catalog(catalog_id)

    return flask.redirect('/')


@app.route('/cataloglist/json', methods=['GET'])
def catalog_list_json_endpoint():
    """Returns list of catalogs in JSON form"""
    return dumps(models.get_catalog_list_dict(), default=models.json_serial)

@app.route('/catalog/<catalog_id>/json', methods=['GET'])
def catalog_json_endpoint(catalog_id):
    """Returns catalog info  in JSON form
    Parameters:
    - catalog_id: integer id of catalog to return
    """
    return dumps(models.get_catalog_dict(int(catalog_id)), default=models.json_serial)
