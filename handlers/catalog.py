import logging
import flask
import models
import login
import uploadfile
import helper
import models

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

