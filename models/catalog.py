import logging
from google.appengine.ext import ndb
from user_login import User, check_user_owns

class Catalog(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    description = ndb.TextProperty(indexed=False)
    cover_picture = ndb.StringProperty(indexed=False)
    owner = ndb.KeyProperty(kind=User, required=True, indexed=True)
    editors = ndb.KeyProperty(kind=User, repeated=True, indexed=True)
    posted = ndb.DateTimeProperty(auto_now_add=True, indexed=True)

    def user_can_edit(self, user):
        return user == self.owner or user in self.editors

def get_catalog_by_id(catalog_id):
    if not catalog_id:
        logging.error('Must pass catalog_id!')
        return None
    return Catalog.get_by_id(catalog_id)

def get_catalogs():
    return Catalog.query()

def delete_catalog(catalog_id):
    catalog_entity = get_catalog_by_id(catalog_id)
    check_user_owns(catalog_entity)
    if not catalog_entity:
        raise ValueError('Catalog not found!')
    catalog_entity.key.delete()

    # TODO: delete related data
