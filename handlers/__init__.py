"""WSGI Routing Handlers"""

from catalog import main_page_handler, catalog_view_handler, add_catalog_handler, edit_catalog_handler, delete_catalog_handler
from category import add_category_handler, edit_category_handler, delete_category_handler
from gconnect import google_login_handler, get_google_credentials, get_google_user_info
from item import add_item_handler, edit_item_handler, delete_item_handler
from logout import logout_handler
from login import login_handler, check_logged_in
from uploadfile import save_file

from responses import success