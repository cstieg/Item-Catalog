"""Catalog Model and related functions"""

import logging
import datetime
from database import get_connection, close_connection


def user_can_edit(user_id, catalog_id):
    """Returns True if given user has edit permission in the catalog"""
    catalog = get_catalog_by_id(catalog_id)

    user_in_editors = False
    if catalog.editors:
        for editor in catalog.editors:
            if editor == user_id:
                user_in_editors = True
                break
    return user_in_editors or user_id == catalog.owner

def add_catalog(name, description, cover_picture, owner):
    connection, cursor = get_connection()
    cursor.execute("""INSERT INTO catalog
                    (name, description, cover_picture, owner, posted)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING *""",
                    (name, description, cover_picture, owner, datetime.datetime.now()))
    catalog = cursor.fetchone()
    connection.commit()
    close_connection(connection, cursor)
    return catalog

def edit_catalog(catalog_id, name, description, cover_picture, owner):
    if not get_catalog_by_id(catalog_id):
        raise ValueError('Catalog id not found!')

    connection, cursor = get_connection()
    cursor.execute("""UPDATE catalog SET 
                    name = %s,
                    description = %s,
                    cover_picture = %s
                    WHERE catalog_id = %s""",
                    (name, description, cover_picture, catalog_id))
    connection.commit()
    close_connection(connection, cursor)

def get_catalog_by_id(catalog_id):
    """Returns catalog entity of a given integer id"""
    if not catalog_id:
        logging.error('Must pass catalog_id!')
        return None

    connection, cursor = get_connection()
    cursor.execute("""SELECT * FROM catalog
                    WHERE catalog_id = %s""", (catalog_id,))

    catalog = cursor.fetchone()
    close_connection(connection, cursor)
    return catalog


def get_catalogs():
    """Returns a query of all catalogs"""
    connection, cursor = get_connection()
    cursor.execute("""SELECT * FROM catalog""")

    catalogs = cursor.fetchall()
    close_connection(connection, cursor)
    return catalogs

def get_catalog_list_dict():
    """Returns a list of catalogs in dict form"""
    return get_catalogs()

def get_catalog_dict(catalog_id):
    """Returns a dict representation of the catalog entity
    Parameter:
    - catalog_id: Integer id of catalog"""
    return get_catalog_by_id(catalog_id)

def delete_catalog(catalog_id):
    """Deletes the catalog with the specified integer id, as well as any categories
    or items in the catalog"""
    catalog_entity = get_catalog_by_id(catalog_id)
    if not catalog_entity:
        raise ValueError('Catalog not found!')

    connection, cursor = get_connection()
    cursor.execute("""DELETE FROM catalog
                    WHERE catalog_id = %s""", (catalog_id,))
    connection.commit()
    close_connection(connection, cursor)
