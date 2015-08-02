#!/usr/bin/env python
import datetime
import json
import models
import util
import webapp2


# it seems that webapp2 doesn't support HTTP method PATCH
# so, the following code monkey patchs the webapp2 to allow it.
# (more information at https://code.google.com/p/webapp-improved/issues/detail?id=69)
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods


# modifiable fields for a Restaurant through PATCH /api/restaurant/<key>
REST_PATCH_ALLOWED_FIELDS = ["name", "email", "password", "owner"]
# modifiable fields for a Customer through PATCH /api/customer/<key>
CUST_PATCH_ALLOWED_FIELDS = ["name", "password", "phone", "email"]
# modifiable fields for a Customer through PATCH /api/restaurant/<rest_key>/order/<order_key>
ORDER_PATCH_ALLOWED_FIELDS = ["completed"]


class RestaurantList(webapp2.RequestHandler):
    def get(self):
        restaurants = models.Restaurant.get_restaurants()
        # TODO: write some code to handle HTTP headers (they're really important, man)
        self.response.headers["Content-Type"] = "application/json"
        self.response.out.write(json.dumps(restaurants, cls=util.JSONEncoder))

    def post(self):
        # turns the json request data, str, into a dict
        data = json.loads(self.request.body)
        # creates a new Restaurant
        new = models.Restaurant()
        # creates its attributes
        new.email = data["email"]
        new.password = data["password"]
        new.name = data["name"]
        # DEV-ONLY: creates new Owner
        owner = models.Owner()
        owner_data = data["owner"]
        owner.name = owner_data['name']
        owner.cpf = owner_data['cpf']
        owner.birthday = datetime.datetime.strptime(owner_data['birthday'], "%m-%d-%Y")

        # persists the new Owner
        models.Owner.create_owner(owner)
        
        new.owner = owner

        if self.request.get('menu'):
            new.menu = self.request.get('menu')

        # persists the new Restaurant
        models.Restaurant.save_restaurant(new)

        output = {}
        output["message"] = "Restaurant Created."
        self.response.out.write(json.dumps(output))


class Restaurant(webapp2.RequestHandler):
    def get(self, restaurant_key):
        # tries to query the Restaurant whose Key is specified in the url path
        # note: the key in url path MUST BE in a urlsafe form
        try:
            restaurant = models.Restaurant.get_restaurants(restaurant_key)
            if restaurant:
                self.response.out.write(json.dumps(restaurant, cls=util.JSONEncoder))
            else:
                self.response.out.write(json.dumps({"message":"There's no such Restaurant. Try again."}))
        # well, you know...
        # shit happens
        # TODO: write this apart, as a decent error handler
        except Exception, e:
            output = {}
            output["message"] = "Something went really, really bad. Try again."
            output["error_message"] = e.message
            self.response.out.write(json.dumps(output))

    def delete(self, restaurant_key):
        try:
            models.Restaurant.delete_restaurant(restaurant_key)
            self.response.out.write("Hasta la vista, baby!")
        except Exception, e:
            output = {}
            output["message"] = "Something went really, really bad. Try again."
            output["error_message"] = e.message
            self.response.out.write(json.dumps(output))

    # operations allowed for PATCH /api/restaurant/<key>
    # - replace
    def patch(self, restaurant_key):
        try:
            # tries to retrieve the Restaurant
            restaurant = models.Restaurant.get_restaurants(restaurant_key)
            if restaurant:
                # gets the request data that describes the operation
                patch_info = json.loads(self.request.body)
                # checks if the given path is a modifiable attribute
                if patch_info["path"][1:] in REST_PATCH_ALLOWED_FIELDS:
                    # replaces the attribute
                    setattr(restaurant, patch_info["path"][1:], patch_info["value"])
                    if models.Restaurant.save_restaurant(restaurant):
                        # and save it
                        self.response.out.write(json.dumps({"msg": "Changes were applied to the Restaurant"}))
        except Exception, e:
            output = {}
            output["message"] = "Something went really, really bad. Try again."
            output["error_message"] = e.message
            self.response.out.write(json.dumps(output))


class Menu(webapp2.RequestHandler):
    def get(self, restaurant_key):
        restaurant = models.Restaurant.get_restaurants(restaurant_key)
        menu = restaurant.menu
        self.response.headers["Content-Type"] = "application/json"
        self.response.out.write(json.dumps(menu, cls=util.JSONEncoder))

    def post(self, restaurant_key):
        # gets the restaurant
        try:
            restaurant = models.Restaurant.get_restaurants(restaurant_key)
        except Exception, e:
            output = {}
            output["message"] = "Something went really, really wrong. Try again."
            output["error_message"] = e.message
            self.response.out.write(json.dumps(output))
        item_data = json.loads(self.request.body)
        # creates a new Item Menu
        new = models.ItemMenu()
        new.name = item_data["name"]
        new.price = float(item_data["price"])
        new.description = item_data["description"]
        models.ItemMenu.save_item_menu(new)
        # adds the new item to the menu
        restaurant.menu.append(new.key)
        # persists the restaurant with modified menu
        models.Restaurant.save_restaurant(restaurant)
        self.response.out.write("Yay! Your request has been processed!")


class ItemMenu(webapp2.RequestHandler):
    def get(self, restaurant_key, item_menu_key):
        self.response.headers["Content-Type"] = "application/json"
        try:
            item_menu = models.ItemMenu.get_item_menu(item_menu_key)
        except Exception, e:
            output = {}
            output["message"] = "No Item Menu with this key, sorry."
            output["error_message"] = e.message
            self.response.out.write(json.dumps(output))
        self.response.out.write(json.dumps(item_menu, cls=util.JSONEncoder))

    def put(self, restaurant_key, item_menu_key):
        # gets the item menu
        try:
            item_menu = models.ItemMenu.get_item_menu(item_menu_key)
        except Exception, e:
            output = {}
            output["message"] = "No Item Menu with this key, sorry."
            output["error_message"] = e.message
            self.response.out.write(json.dumps(output))
        item_data = json.loads(self.request.body)
        # update all data
        item_menu.name = item_data["name"]
        item_menu.price = float(item_data["price"])
        item_menu.description = item_data["description"]
        # put it
        models.ItemMenu.save_item_menu(item_menu)

        self.response.out.write("Yay! Your request has been processed!")

    def delete(self, restaurant_key, item_menu_key):
        try:
            models.Restaurant.delete_restaurant(item_menu_key)
            self.response.out.write("Hasta la vista, baby!")
        except Exception, e:
            output = {}
            output["message"] = "Something went really, really bad. Try again."
            output["error_message"] = e.message
            self.response.out.write(json.dumps(output))


class CustomerList(webapp2.RequestHandler):
    def get(self):
        customers = models.Customer.get_customer()
        self.response.out.headers["Content-Type"] = 'application/json'
        self.response.out.write(json.dumps(customers, cls=util.JSONEncoder))

    def post(self):
        data = json.loads(self.request.body)
        new = models.Customer()
        new.name = data["name"]
        new.phone = data["phone"]
        new.password = data["password"]
        new.email = data["email"]

        output = {}
        try:
            models.Customer.save_customer(new)
            output["message"] = "Success! You are now one of us, Tobby!"
        except Exception, e:
            output["message"] = "Something went really, really bad. Try again."
            output["error_message"] = e.message

        self.response.out.write(json.dumps(output))


class Customer(webapp2.RequestHandler):
    def get(self, customer_key):
        try:
            customer = models.Customer.get_customer(customer_key)
            if not customer: raise Exception
            self.response.out.write(json.dumps(customer, cls=util.JSONEncoder))
        except Exception, e:
            output = {}
            output["message"] = "Sorry. We don't know this person you're looking for. Try: http://www.google.com."
            output["error_message"] = e.message
            self.response.out.write(json.dumps(output))

    # allowed operations:
    #   - replace
    def patch(self, customer_key):
        try:
            customer = models.Customer.get_customer(customer_key)
            if customer:
                patch_info = json.loads(self.request.body)
                if patch_info["path"][1:] in CUST_PATCH_ALLOWED_FIELDS:
                    setattr(customer, patch_info["path"][1:], patch_info["value"])
                    if models.Customer.save_customer(customer):
                        self.response.out.write(json.dumps({"message": "Customer updated successfully"}))
        except Exception, e:
            output = {}
            output["message"] = "Something went really, really bad. Try again."
            output["error_message"] = e.message
            self.response.out.write(json.dumps(output))

    def delete(self, customer_key):
        output = {}
        try:
            models.Customer.delete_restaurant(customer_key)
            output["message"] = "Rest in peace, honey."
        except Exception, e:
            output["message"] = "Sorry. We don't know this person you're looking for. Try: http://www.google.com."
            output["error_message"] = e.message
        self.response.out.write(json.dumps(output))


class OrderListByRestaurant(webapp2.RequestHandler):
    def get(self, restaurant_key):
        restaurant = models.Restaurant.get_restaurants(restaurant_key)
        orders = restaurant.orders
        self.response.out.write(json.dumps(orders, cls=util.JSONEncoder))

    def post(self, restaurant_key):
        restaurant = models.Restaurant.get_restaurants(restaurant_key)
        output = {}
        if restaurant:
            order_data = json.loads(self.request.body)
            new = models.Order()
            new.completed = False

            for item_key in order_data["items"]:
                item = models.ItemMenu.get_item_menu(item_key)
                new.items.append(item.key)

            # persists the new order
            models.Order.save_order(new)
            # append the new order to the restaurant:
            restaurant.orders.append(new.key)
            models.Restaurant.save_restaurant(restaurant)
            # appends the new order to the customer:
            customer = models.Customer.get_customer(order_data["customer"])
            customer.orders.append(new.key)
            models.Customer.save_customer(customer)

            output["message"] = "Your order has been placed!"
            self.response.out.write(json.dumps(output))
        else:
            output["message"] = "Something went really, really bad. Try again."
            self.response.out.write(json.dumps(output))


class OrderListByCustomer(webapp2.RequestHandler):
    def get(self, customer_key):
        customer = models.Customer.get_customer(customer_key)
        if customer:
            orders = customer.orders
            self.response.out.write(json.dumps(orders, cls=util.JSONEncoder))
        else:
            output = {}
            output["message"] = "Something went really, really bad. Try again."
            self.response.out.write(json.dumps(output))


class Order(webapp2.RequestHandler):
    def get(self, restaurant_key, order_key):
        restaurant = models.Restaurant.get_restaurants(restaurant_key)
        order = models.Order.get_order(order_key)
        if restaurant and order:
            self.response.out.write(json.dumps(order, cls=util.JSONEncoder))
        else:
            output = {}
            output["message"] = "No orders for you, Eugene."

    # allowed operations:
    #   - replace
    def patch(self, restaurant_key, order_key):
        try:
            order = models.Order.get_order(order_key)
            if order:
                patch_info = json.loads(self.request.body)
                if patch_info["path"][1:] in ORDER_PATCH_ALLOWED_FIELDS:
                    setattr(order, patch_info["path"][1:], bool(patch_info["value"]))
                    models.Order.save_order(order)
                    self.response.out.write(json.dumps({"message": "Order updated successfully"}))
        except Exception, e:
            output = {}
            output["message"] = "Something went really, really bad. Try again."
            output["error_message"] = e.message
            self.response.out.write(json.dumps(output))