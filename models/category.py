import logging
from google.appengine.ext import ndb
import catalog

class Category(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    description = ndb.TextProperty(indexed=False)
    catalog = ndb.KeyProperty(kind=catalog.Catalog, required=True, indexed=True)
    posted = ndb.DateProperty(auto_now_add=True, indexed=True)


def get_categories(catalog_id, category_id=None):
    if not catalog_id:
        raise ValueError('catalog_id is required!')
    catalog_entity = catalog.get_catalogs(catalog_id)
    if not catalog_entity:
        logging.error('Catalog not found!')
        return None
    if category_id:
        category_entity = Category.get_by_id(category_id)
        if category_entity.catalog != catalog_entity.key:
            logging.error('Category does not match catalog!')
        return category_entity
    return Category.query(Category.catalog == catalog_entity.key)
