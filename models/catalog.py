from google.appengine.ext import ndb
from user_login import User

class Catalog(ndb.Model):
    name = ndb.StringProperty(required=True, indexed=True)
    description = ndb.TextProperty(indexed=False)
    cover_picture = ndb.StringProperty(indexed=False)
    owner = ndb.KeyProperty(kind=User, required=True, indexed=True)
    editors = ndb.KeyProperty(kind=User, repeated=True, indexed=True)
    posted = ndb.DateTimeProperty(auto_now_add=True, indexed=True)

    def user_can_edit(self, user):
        return user == self.owner or user in self.editors
