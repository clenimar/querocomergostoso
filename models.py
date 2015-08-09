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
    def save_item_menu(self, item):
        """Save the item, if doesn't exist, or update it, if exists"""
        if isinstance(item, ItemMenu):
            item.put()
            return True
        return False

    @classmethod
    def get_item_menu(self, item_menu_key):
        """Returns a item menu , given a valid key."""
        query = ItemMenu.query(ItemMenu.key == ndb.Key(urlsafe = item_menu_key))
        return query.get()

    @classmethod
    def delete_item_menu(self, item_menu_key):
        """Deletes a Restaurant, given a valid key.
        Invalid keys will lead to an exception"""
        try:
            whosgonnadie = ItemMenu.query(ItemMenu.key == ndb.Key(urlsafe=item_menu_key))
            whosgonnadie.delete()
        except Exception, e:
            output = {}
            output["message"] = "Well... it's embarassing. I don't know that happent. Sorry."
            output["error_message"] = e.message
            return output


class Order(ndb.Model):
    items = ndb.KeyProperty(ItemMenu, repeated=True)
    completed = ndb.BooleanProperty()

    @classmethod
    def save_order(cls, new):
        if isinstance(new, Order):
            new.put()

    @classmethod
    def get_order(cls, order_key=None):
        if order_key:
            query = Order.query(Order.key == ndb.Key(urlsafe=order_key))
            return query.get()
        return Order.query().fetch(20)

    @classmethod
    def delete_order(cls, order_key):
        poorfella = Order.query(Order.key == ndb.Key(urlsafe=order_key))
        if poorfella:
            poorfella.delete()

    @staticmethod
    def get_status(self):
        return self.completed

    @staticmethod
    def set_status(self, new):
        self.completed = new


class Customer(ndb.Model):
    email = ndb.StringProperty()
    password = ndb.StringProperty()
    name = ndb.StringProperty()
    phone = ndb.StringProperty()
    orders = ndb.KeyProperty(kind=Order, repeated=True)

    @classmethod
    def save_customer(cls, new):
        if isinstance(new, Customer):
            new.put()
            return True
        return False

    @classmethod
    def get_customer(cls, customer_key=None):
        if customer_key:
            query = Customer.query(Customer.key == ndb.Key(urlsafe=customer_key))
            return query.get()
        return Customer.query().fetch(20)

    @classmethod
    def delete_restaurant(cls, customer_key):
        stalin_sends_regards = Customer.query(Customer.key == ndb.Key(urlsafe=customer_key))
        if stalin_sends_regards:
            stalin_sends_regards.delete()


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
    menu = ndb.KeyProperty(ItemMenu, repeated=True)
    orders = ndb.KeyProperty(kind=Order, repeated=True)

    @classmethod
    def get_restaurants(self, restaurant_key=None):
        """Returns a Restaurant, given a valid key.
        Give it no key and it'll return all the Restaurants"""
        if restaurant_key:
            query = Restaurant.query(Restaurant.key == ndb.Key(urlsafe=restaurant_key))
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
    def delete_restaurant(self, restaurant_key):
        """Deletes a Restaurant, given a valid key.
        Invalid keys will lead to an exception"""
        try:
            whosgonnadie = Restaurant.query(Restaurant.key == ndb.Key(urlsafe=restaurant_key))
            if whosgonnadie:
                whosgonnadie.delete()
        except Exception, e:
            output = {}
            output["message"] = "Well... it's embarassing. I don't know that happent. Sorry."
            output["error_message"] = e.message
            return output
