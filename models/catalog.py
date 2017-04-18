
import logging
from google.appengine.ext import ndb
import user_login
import item
import category

class Catalog(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    description = ndb.TextProperty(indexed=False)
    cover_picture = ndb.StringProperty(indexed=False)
    owner = ndb.KeyProperty(kind=user_login.User, required=True, indexed=True)
    editors = ndb.KeyProperty(kind=user_login.User, repeated=True, indexed=True)
    posted = ndb.DateTimeProperty(auto_now_add=True, indexed=True)

    def user_can_edit(self, user):
        user_in_editors = False
        for editor in self.editors:
            if editor.get() == user:
                user_in_editors = True
                break
        return user_in_editors or user == self.owner.get()

def get_catalog_by_id(catalog_id):
    if not catalog_id:
        logging.error('Must pass catalog_id!')
        return None
    return Catalog.get_by_id(catalog_id)

def get_catalogs():
    return Catalog.query()

def delete_catalog(catalog_id):
    catalog_entity = get_catalog_by_id(catalog_id)
    if not catalog_entity:
        raise ValueError('Catalog not found!')

    for category_entity in category.get_categories(catalog_entity.key.id()):
        category_entity.key.delete()
    for item_entity in item.get_items(catalog_entity.key.id()):
        item_entity.key.delete()

    catalog_entity.key.delete()
