import logging
from time import clock, sleep
from google.appengine.ext import ndb

from user_login import User, create_user, get_current_user, find_user_by_email
from item import Item, get_item_by_id, get_items, delete_item
from category import Category, get_category_by_id, get_categories, delete_category
from catalog import Catalog, get_catalog_by_id, get_catalogs, delete_catalog


def wait_for(entity, incremental_wait_time=0.100, max_wait_time=2.000):
    """Wait for an entity to be updated in the Datastore before proceeding.
    Otherwise, an item may be added but not display when template is rerendered.
    
    Parameters:
        entity - a Datastore entity extending ndb.Model
        incremental_wait_time - the time in seconds to wait at a time
        max_wait_time - the time in seconds to return even if the entity has not been updated
    """
    if not isinstance(entity, ndb.Model):
        raise ValueError('Parameter entity must be instance of ndb.Model!')
    entity_kind = entity.__class__
    if not 'name' in vars(entity_kind):
        raise ValueError('Entity must have name property!')
    start_time = clock()
    while entity_kind.query(entity_kind.name == entity.name).count(1) == 0 and \
                            clock() < start_time + max_wait_time:
        sleep(incremental_wait_time)

