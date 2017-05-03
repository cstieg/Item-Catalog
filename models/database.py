import psycopg2
from psycopg2.extras import NamedTupleCursor


def get_connection():
    """Connect to the PostgreSQL database.  Returns a database connection and cursor in a tuple."""
    connection = psycopg2.connect("dbname=catalog user=postgres password=michigan")

    cursor = connection.cursor(cursor_factory=NamedTupleCursor)
    return (connection, cursor)

def close_connection(connection, cursor):
    """Closes a connection to the PostgreSQL database."""
    cursor.close()
    connection.close()
