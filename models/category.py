"""Category Model and related functions"""

import logging
import datetime
import item
import catalog
from database import get_connection, close_connection

def add_category(name, description, catalog_id):
    connection, cursor = get_connection()
    cursor.execute("""INSERT INTO category
                    (name, description, catalog, posted)
                    VALUES (%s, %s, %s, %s)
                    RETURNING *""",
                    (name, description, catalog_id, datetime.datetime.now()))
    catalog = cursor.fetchone()
    connection.commit()
    close_connection(connection, cursor)
    return catalog

def edit_category(category_id, catalog_id, name, description):
    if not get_category_by_id(catalog_id, category_id):
        raise ValueError('Catalog id not found!')

    connection, cursor = get_connection()
    cursor.execute("""UPDATE category SET 
                    name = %s,
                    description = %s
                    WHERE category_id = %s""",
                    (name, description, category_id))
    connection.commit()
    close_connection(connection, cursor)

def get_items(catalog_id, category_id):
    """Returns a query of the items in the category"""
    return item.get_items(catalog_id, category_id)

def get_category_by_id(catalog_id, category_id):
    """Returns the category entity of a given integer catalog id and category id"""

    if not catalog_id:
        raise ValueError('catalog_id is required!')
    if not category_id:
        return None


    connection, cursor = get_connection()
    cursor.execute("""SELECT * FROM category
                    WHERE catalog = %s AND category_id = %s""", (catalog_id, category_id))

    category = cursor.fetchone()
    close_connection(connection, cursor)
    return category


def get_categories(catalog_id):
    """Returns a query of all the categories of a given catalog"""
    if not catalog_id:
        raise ValueError('catalog_id is required!')

    catalog_entity = catalog.get_catalog_by_id(catalog_id)
    if not catalog_entity:
        logging.error('Catalog not found!')
        return None

    connection, cursor = get_connection()
    cursor.execute("""SELECT * FROM category
                    WHERE catalog = %s""", (catalog_id,))

    categories = cursor.fetchall()
    close_connection(connection, cursor)
    return categories


def get_category_dict(catalog_id, category_id):
    """Returns a dict representation of a category of given catalog and category id"""
    return get_category_by_id(catalog_id, category_id)

def delete_category(catalog_id, category_id):
    """Deletes a category of a given catalog id and category id, as well as any
    items in that category"""
    if not catalog_id or not category_id:
        raise ValueError('Must pass a valid catalog!')
    category_entity = get_category_by_id(catalog_id, category_id)
    if not category_entity:
        raise ValueError('Category not found!')

    connection, cursor = get_connection()
    cursor.execute("""DELETE FROM category
                    WHERE catalog = %s AND category_id = %s""", (catalog_id, category_id))
    connection.commit()
    close_connection(connection, cursor)

