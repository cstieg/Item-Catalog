import logging
from google.appengine.ext import ndb
import catalog
import item

class Category(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    description = ndb.TextProperty(indexed=False)
    catalog = ndb.KeyProperty(kind=catalog.Catalog, required=True, indexed=True)
    posted = ndb.DateProperty(auto_now_add=True, indexed=True)

    def get_items(self):
        logging.info('Get items')
        logging.info(self.catalog.id())
        logging.info(self.key.id())
        return item.get_items(self.catalog.id(), self.key.id())

def get_category_by_id(catalog_id, category_id):
    if not catalog_id:
        raise ValueError('catalog_id is required!')
    if not category_id:
        return None
    catalog_entity = catalog.Catalog.get_by_id(catalog_id)
    if not catalog_entity:
        logging.error('Catalog not found!')
        return None
    category_entity = Category.get_by_id(category_id)
    if category_entity.catalog != catalog_entity.key:
        logging.error('Category does not match catalog!')
        return None

    return category_entity

def get_categories(catalog_id):
    if not catalog_id:
        raise ValueError('catalog_id is required!')
    catalog_entity = catalog.get_catalog_by_id(catalog_id)
    if not catalog_entity:
        logging.error('Catalog not found!')
        return None
    return Category.query(Category.catalog == catalog_entity.key)

def delete_category(catalog_id, category_id):
    if not catalog_id or not category_id:
        raise ValueError('Must pass a valid catalog!')
    category_entity = get_category_by_id(catalog_id, category_id)
    if not category_entity:
        raise ValueError('Category not found!')

    category_entity.key.delete()

    # TODO: delete related data
