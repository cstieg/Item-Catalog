"""Category Model and related functions"""

import logging
from google.appengine.ext import ndb
import item
import catalog

class Category(ndb.Model):
    """Model of catalog category"""
    name = ndb.StringProperty(required=True, indexed=True)
    description = ndb.TextProperty(indexed=False)
    catalog = ndb.KeyProperty(kind=catalog.Catalog, required=True, indexed=True)
    posted = ndb.DateProperty(auto_now_add=True, indexed=True)

    def get_items(self):
        """Returns a query of the items in the category"""
        return item.get_items(self.catalog.id(), self.key.id())

def get_category_by_id(catalog_id, category_id):
    """Returns the category entity of a given integer catalog id and category id"""
    if not catalog_id:
        raise ValueError('catalog_id is required!')
    if not category_id:
        return None

    catalog_entity = catalog.get_catalog_by_id(catalog_id)
    if not catalog_entity:
        logging.error('Catalog not found!')
        return None

    category_entity = Category.get_by_id(category_id)
    if category_entity.catalog != catalog_entity.key:
        logging.error('Category does not match catalog!')
        return None

    return category_entity

def get_categories(catalog_id):
    """Returns a query of all the categories of a given catalog"""
    if not catalog_id:
        raise ValueError('catalog_id is required!')

    catalog_entity = catalog.get_catalog_by_id(catalog_id)
    if not catalog_entity:
        logging.error('Catalog not found!')
        return None

    return Category.query(Category.catalog == catalog_entity.key)

def get_category_dict(catalog_id, category_id):
    """Returns a dict representation of a category of given catalog and category id"""
    category_dict = get_category_by_id(catalog_id, category_id).to_dict()
    items = []
    for item_entity in item.get_items(catalog_id, category_id):
        items.append(item_entity.to_dict())
    category_dict['items'] = items
    return category_dict

def delete_category(catalog_id, category_id):
    """Deletes a category of a given catalog id and category id, as well as any
    items in that category"""
    if not catalog_id or not category_id:
        raise ValueError('Must pass a valid catalog!')
    category_entity = get_category_by_id(catalog_id, category_id)
    if not category_entity:
        raise ValueError('Category not found!')

    catalog_entity = catalog.get_catalog_by_id(catalog_id)

    for item_entity in item.get_items(catalog_entity.key.id(), category_entity.key.id()):
        item_entity.key.delete()
    category_entity.key.delete()
