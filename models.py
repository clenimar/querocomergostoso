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

    @classmethod
    def save_item(self, item):
        if isinstance(item, ItemMenu):
            item.put()
            return True
        return False


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

    @classmethod
    def get_restaurants(self, restaurant_key=None):
        """Returns a Restaurant, given a valid key.
        Give it no key and it'll return all the Restaurants"""
        if restaurant_key:
            query = ndb.Key(urlsafe=restaurant_key)
            return query.get()
        return Restaurant.query().fetch(20)

    @classmethod
    def save_restaurant(self, new):
        """Puts a new Restaurant into datastore.
        Returns True if success, False otherwise"""
        if isinstance(new, Restaurant):
            new.put()
            return True
        return False

    @classmethod
    def delete_restaurant(self, key):
        """Deletes a Restaurant, given a valid key.
        Invalid keys will lead to an exception"""
        try:
            whosgonnadie = ndb.Key(urlsafe=key)
            whosgonnadie.delete()
        except Exception, e:
            output = {}
            output["message"] = "Well... it's embarassing. I don't know that happent. Sorry."
            output["error_message"] = e.message
            return output




