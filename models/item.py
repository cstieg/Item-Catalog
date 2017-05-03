"""Item Model and related functions"""

import logging
import datetime
import category
import catalog
from database import get_connection, close_connection

def add_item(name, description, price, picture, owner, catalog_id, category_id):
    connection, cursor = get_connection()
    cursor.execute("""INSERT INTO item
                    (name, description, price, picture, owner, catalog, category, posted)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING *""",
                    (name, description, price, picture, owner, catalog_id, category_id, datetime.datetime.now()))
    catalog = cursor.fetchone()
    connection.commit()
    close_connection(connection, cursor)
    return catalog

def edit_item(item_id, name, description, price, picture, catalog_id, category_id):
    if not get_item_by_id(catalog_id, item_id):
        raise ValueError('Item id not found!')

    connection, cursor = get_connection()
    cursor.execute("""UPDATE item SET 
                    name = %s,
                    description = %s,
                    price = %s,
                    picture = %s,
                    category = %s
                    WHERE item_id = %s""",
                    (name, description, price, picture, category_id, item_id))
    connection.commit()
    close_connection(connection, cursor)


def get_item_by_id(catalog_id, item_id):
    """Returns the item entity of a given catalog id and item id"""
    if not catalog_id:
        raise ValueError('catalog_id is required!')
    if not item_id:
        raise ValueError('item_id is required!')

    catalog_entity = catalog.get_catalog_by_id(catalog_id)
    if not catalog_entity:
        logging.error('Catalog not found!')
        return None

    connection, cursor = get_connection()
    cursor.execute("""SELECT * FROM item
                    WHERE catalog = %s AND item_id = %s""", (catalog_id, item_id))

    item = cursor.fetchone()
    close_connection(connection, cursor)

    return item

def get_items(catalog_id, category_id=None):
    """Returns a query of the items of a given catalog, and optionally, a given
    category in that catalog"""
    if not catalog_id:
        raise ValueError('catalog_id is required!')

    catalog_entity = catalog.get_catalog_by_id(catalog_id)
    if not catalog_entity:
        logging.error('Catalog not found!')
        return None

    connection, cursor = get_connection()
    if category_id:
        category_entity = category.get_category_by_id(catalog_id, category_id)
        if not category_entity:
            logging.error('Category not found!')
            return None

        cursor.execute("""SELECT * FROM item
                        WHERE catalog = %s AND category = %s""", (catalog_id, category_id))
    else:
        cursor.execute("""SELECT * FROM item
                        WHERE catalog = %s""", (catalog_id))

    items = cursor.fetchall()
    close_connection(connection, cursor)
    return items

def get_item_dict(catalog_id, item_id):
    """Returns a dict representation of an item of given catalog and item id"""
    return get_item_by_id(catalog_id, item_id)

def delete_item(catalog_id, item_id):
    """Deletes an item of a given catalog id and item id"""
    if not catalog_id or not item_id:
        raise ValueError('Must pass a valid item!')

    connection, cursor = get_connection()
    cursor.execute("""DELETE FROM item
                    WHERE catalog = %s AND item_id = %s""", (catalog_id, item_id))
    connection.commit()
    close_connection(connection, cursor)
