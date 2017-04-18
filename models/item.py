import logging
from google.appengine.ext import ndb
import user_login
import category
import catalog

class Item(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    description = ndb.TextProperty(indexed=False)
    price = ndb.FloatProperty(indexed=True)
    picture = ndb.StringProperty(indexed=False)
    owner = ndb.KeyProperty(kind=user_login.User, required=True, indexed=True)
    catalog = ndb.KeyProperty(kind=catalog.Catalog, required=True, indexed=True)
    category = ndb.KeyProperty(kind=category.Category, indexed=True)
    posted = ndb.DateTimeProperty(auto_now_add=True, indexed=True)

def get_item_by_id(catalog_id, item_id):
    # find catalog
    if not catalog_id:
        raise ValueError('catalog_id is required!')
    if not item_id:
        raise ValueError('item_id is required!')
    catalog_entity = catalog.get_catalog_by_id(catalog_id)
    if not catalog_entity:
        logging.error('Catalog not found!')
        return None

    # find item
    item_entity = Item.get_by_id(item_id)

    if not item_entity:
        logging.error('Item not found!')
        return None
    if item_entity.catalog != catalog_entity.key:
        logging.error('Item does not match catalog!')
        return None

    return item_entity

def get_items(catalog_id, category_id=None):
    # find catalog
    if not catalog_id:
        raise ValueError('catalog_id is required!')
    catalog_entity = catalog.get_catalog_by_id(catalog_id)
    if not catalog_entity:
        logging.error('Catalog not found!')
        return None

    # find category
    if category_id:
        category_entity = category.get_category_by_id(catalog_id, category_id)
        if not category_entity:
            logging.error('Category not found!')
            return None
        if category_entity.catalog != catalog_entity.key:
            logging.error('Category does not match catalog!')
            return None
        q = Item.query(Item.category == category_entity.key)
        return q
    else:
        return Item.query(Item.catalog == catalog_entity.key)


def delete_item(catalog_id, item_id):
    if not catalog_id or not item_id:
        raise ValueError('Must pass a valid item!')
    item_entity = Item.get_by_id(item_id)
    if not item_entity:
        raise ValueError('Item not found!')

    item_entity.key.delete()

    # TODO: delete related data
