from google.appengine.ext import ndb
from catalog import Catalog

class Category(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    description = ndb.TextProperty(indexed=False)
    catalog = ndb.KeyProperty(kind=Catalog, required=True, indexed=True)
    posted = ndb.DateProperty(auto_now_add=True, indexed=True)
