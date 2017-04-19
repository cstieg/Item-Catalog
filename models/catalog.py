"""Catalog Model and related functions"""

import logging
from google.appengine.ext import ndb
import user_login
import item
import category

class Catalog(ndb.Model):
    """Model of item catalog"""
    name = ndb.StringProperty(required=True, indexed=True)
    description = ndb.TextProperty(indexed=False)
    cover_picture = ndb.StringProperty(indexed=False)
    owner = ndb.KeyProperty(kind=user_login.User, required=True, indexed=True)
    editors = ndb.KeyProperty(kind=user_login.User, repeated=True, indexed=True)
    posted = ndb.DateTimeProperty(auto_now_add=True, indexed=True)

    def user_can_edit(self, user):
        """Returns True if given user has edit permission in the catalog"""
        user_in_editors = False
        for editor in self.editors:
            if editor.get() == user:
                user_in_editors = True
                break
        return user_in_editors or user == self.owner.get()

def get_catalog_by_id(catalog_id):
    """Returns catalog entity of a given integer id"""
    if not catalog_id:
        logging.error('Must pass catalog_id!')
        return None
    return Catalog.get_by_id(catalog_id)

def get_catalogs():
    """Returns a query of all catalogs"""
    return Catalog.query()

def get_catalog_list_dict():
    """Returns a list of catalogs in dict form"""
    catalog_list = []
    for catalog_entity in get_catalogs():
        catalog_list.append(catalog_entity.to_dict())
    return catalog_list

def get_catalog_dict(catalog_id):
    """Returns a dict representation of the catalog entity
    Parameter:
    - catalog_id: Integer id of catalog"""
    catalog_dict = get_catalog_by_id(catalog_id).to_dict()
    categories = []
    for category_entity in category.get_categories(catalog_id):
        categories.append(category.get_category_dict(catalog_id, category_entity.key.id()))
    catalog_dict['categories'] = categories
    return catalog_dict

def delete_catalog(catalog_id):
    """Deletes the catalog with the specified integer id, as well as any categories
    or items in the catalog"""
    catalog_entity = get_catalog_by_id(catalog_id)
    if not catalog_entity:
        raise ValueError('Catalog not found!')

    for category_entity in category.get_categories(catalog_entity.key.id()):
        category_entity.key.delete()
    for item_entity in item.get_items(catalog_entity.key.id()):
        item_entity.key.delete()

    catalog_entity.key.delete()
