import logging
import flask
import models
import login
import uploadfile
import helper
from models import User

def add_new_catalog(form_data, files):
    logging.info(form_data)
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
        return helper.success_response()
    except IOError:
        return ('Failed to add new catalog', 401)

