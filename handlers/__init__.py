"""WSGI Routing Handlers"""

from decorators import check_logged_in
from catalog import main_page_handler, catalog_view_handler, add_catalog_handler, edit_catalog_handler, delete_catalog_handler
from category import add_category_handler, edit_category_handler, delete_category_handler
from gconnect import google_login_handler, get_google_credentials, get_google_user_info
from item import add_item_handler, edit_item_handler, delete_item_handler
from logout import logout_handler
from login import login_handler
from uploadfile import save_file

from responses import success

from itemcatalog import app

import models

@app.context_processor
def context_processor_func():
    return dict(user_can_edit=models.user_can_edit,
                get_items_in_category=models.get_items)
