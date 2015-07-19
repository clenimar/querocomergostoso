#!/usr/bin/env python
from google.appengine.ext import ndb


class Owner(ndb.Model):
    name = ndb.StringProperty()
    cpf = ndb.StringProperty()
    birthday = ndb.DateProperty()

    @staticmethod
    def create_owner(new):
        new.put()


class ItemMenu(ndb.Model):
    name = ndb.StringProperty()
    description = ndb.TextProperty()
    price = ndb.FloatProperty()


class Order(ndb.Model):
    items = ndb.StructuredProperty(ItemMenu, repeated=True)


class Customer(ndb.Model):
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    name = ndb.StringProperty()
    phone = ndb.StringProperty()
    orders = ndb.KeyProperty(kind=Order, repeated=True)


class Address(ndb.Model):
    street = ndb.StringProperty()
    number = ndb.IntegerProperty()
    district = ndb.StringProperty()
    postal_code = ndb.StringProperty()
    complement = ndb.StringProperty()


class Restaurant(ndb.Model):
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    name = ndb.StringProperty()
    owner = ndb.StructuredProperty(Owner)
    menu = ndb.StructuredProperty(ItemMenu, repeated=True)
    orders = ndb.KeyProperty(kind=Order, repeated=True)

    @staticmethod
    def get_restaurants(restaurant_id=None):
        return Restaurant.query().get().to_dict()

    @staticmethod
    def create_restaurant(new):
        new.put()

