"""User Model and related functions"""
import flask
import datetime

from database import get_connection, close_connection



def find_user_by_email(email):
    """Returns the user entity corresponding to an email address"""
    if not email:
        return None
    connection, cursor = get_connection()
    cursor.execute("""SELECT * FROM catalog_user
                    WHERE username = %s""", (email,))
    user = cursor.fetchone()
    print user
    close_connection(connection, cursor)
    return user

def create_user(email, name, provider, picture):
    """Creates or updates a user entity with the parameters
    Returns a dict object of the user"""
    username = email
    connection, cursor = get_connection()
    cursor.execute("""INSERT INTO catalog_user (username, full_name, email, provider, picture, signed_up)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (username) DO UPDATE SET
                    full_name = EXCLUDED.full_name,
                    email = EXCLUDED.email,
                    provider = EXCLUDED.provider,
                    picture = EXCLUDED.picture,
                    signed_up = EXCLUDED.signed_up
                    RETURNING *;""",
                    (username, name, email, provider, picture, datetime.datetime.now()))
    user = cursor.fetchone()
    connection.commit()
    close_connection(connection, cursor)
    return user

def get_current_user():
    """Returns the user entity currently logged in"""
    return find_user_by_email(flask.session.get('email'))
