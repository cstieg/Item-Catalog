import logging
import flask
import models
import login
import uploadfile
import helper
import models
from werkzeug.exceptions import BadRequest
from helper import success_response

def catalog_view(catalog_id):
    username = flask.session.get('username')
    catalog = models.get_catalogs(int(catalog_id))
    if not catalog:
        flask.flash('Could not find catalog with id %s!' % catalog_id)
    return flask.render_template('catalog.html', username=username, catalog=catalog)

def add_new_catalog(form_data, files):
    try:
        cover_picture_obj = files.get('cover_picture')
        cover_picture_url = uploadfile.save_file(cover_picture_obj)
        owner = login.get_current_user()
        owner_key = owner.key
        name = form_data.get('name')
        description = form_data.get('description')

        new_catalog = models.Catalog(name=name,
                                     description=description,
                                     cover_picture=cover_picture_url,
                                     owner=owner_key)
        new_catalog.put()
        return flask.redirect('/catalog/%d' % new_catalog.key.id())
    except IOError:
        return ('Failed to add new catalog', 401)

def edit_catalog_view(catalog_id):
    username = flask.session.get('username')
    catalog = models.get_catalogs(int(catalog_id))
    if not catalog:
        flask.flash('Could not find catalog with id %s!' % catalog_id)
    return flask.render_template('editcatalog.html', username=username, catalog=catalog)

def edit_catalog(catalog_id, form_data, files):
    try:
        catalog = models.get_catalogs(int(catalog_id))

        cover_picture_obj = files.get('cover_picture')
        # TODO: delete old picture
        catalog.cover_picture = uploadfile.save_file(cover_picture_obj)
        catalog.name = form_data.get('name')
        catalog.description = form_data.get('description')

        catalog.put()
        return flask.redirect('/catalog/%d' % catalog.key.id())
    except IOError:
        return ('Failed to edit catalog', 401)

def delete_catalog(catalog_id):
    username = flask.session.get('username')
    catalog = models.get_catalogs(int(catalog_id))
    if not catalog:
        flask.flash('Could not find catalog with id %s!' % catalog_id)
        raise BadRequest
    models.delete_catalog(int(catalog_id))
    return flask.redirect('/')