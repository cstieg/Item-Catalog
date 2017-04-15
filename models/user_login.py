from google.appengine.ext import ndb

# TODO: Add validators for entity fields

class User(ndb.Model):
    """Users registered to create content and comment and like on the blog"""
    username = ndb.StringProperty(required=True, indexed=True)
    full_name = ndb.StringProperty(indexed=False)
    password = ndb.StringProperty(indexed=False)
    signedUp = ndb.DateTimeProperty(auto_now_add=True, indexed=True)
    email = ndb.StringProperty(indexed=True)
    provider = ndb.StringProperty(indexed=True)
    picture = ndb.StringProperty(indexed=False)

def find_user_by_email(email):
    return User.query(User.email == email).get()

def create_user(email, name, provider, picture):
    existing_user = find_user_by_email(email)

    if existing_user:
        existing_user.username = email
        existing_user.full_name = name
        existing_user.email = email
        existing_user.provider = provider
        existing_user.picture = picture
        return existing_user.put()
    else:
        new_user = User(
                    username=email,
                    full_name=name,
                    email=email,
                    provider=provider,
                    picture=picture)
        return new_user.put()
