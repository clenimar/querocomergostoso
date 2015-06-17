from google.appengine.ext import ndb

class Owner(ndb.Model):
    name = ndb.StringProperty()
    CPF = ndb.StringProperty()
    birthday = ndb.DateProperty()

class ItemMenu(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    price = ndb.FloatProperty()

class Address(ndb.Model):
    street = ndb.StringProperty()
    number = ndb.IntegerProperty()
    district = ndb.StringProperty()
    postal_code = ndb.StringProperty()
    complement = ndb.StringProperty()

class Order(ndb.Model):
    client = ndb.StructuredProperty(Client)
    restaurant = ndb.StructuredProperty(Restaurant)
    items = ndb.StructuredProperty(ItemMenu, repeated=True)

class Restaurant(ndb.Model):
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    name = ndb.StringProperty()
    owner = ndb.StructuredProperty(Owner)
    menu = ndb.StructuredProperty(ItemMenu, repeated=True)
    orders = ndb.StructuredProperty(Order, repeated=True)

class Client(ndb.Model):
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    name = ndb.StringProperty()
    phone = ndb.StringProperty()
    orders = ndb.StructuredProperty(Order, repeated=True)

