from google.appengine.ext import ndb
from user_login import User
from category import Category

class Item(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    description = ndb.TextProperty(indexed=False)
    price = ndb.FloatProperty(indexed=True)
    picture = ndb.StringProperty(indexed=False)
    owner = ndb.KeyProperty(kind=User, required=True, indexed=True)
    category = ndb.KeyProperty(kind=Category, required=True, indexed=True)
    posted = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
