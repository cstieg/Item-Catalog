"""Models of the catalog data"""

import logging
from time import clock, sleep
from datetime import date, datetime


from user_login import create_user, get_current_user, find_user_by_email
from item import get_item_by_id, get_items, delete_item, get_item_dict, add_item, edit_item
from category import get_category_by_id, get_categories, delete_category, get_category_dict, add_category, edit_category
from catalog import user_can_edit, get_catalog_by_id, get_catalogs, delete_catalog, get_catalog_dict, get_catalog_list_dict, add_catalog, edit_catalog



def json_serial(obj):
    """Serializes the properties of the dict representation of a Datastore entity
    not able to be handled by the regular json.dumps function"""
    if isinstance(obj, date) or isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable!")



