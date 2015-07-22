#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import datetime
import json
import models
import util
import webapp2


# modifiable fields for a Restaurant through PATCH /api/restaurant/<key>
REST_PATCH_ALLOWED_FIELDS = ["name", "email", "password", "owner"]


class Project(webapp2.RequestHandler):
    def get(self):
        self.response.write('olars.')


class RestaurantList(webapp2.RequestHandler):
    def get(self):
        restaurants = models.Restaurant.get_restaurants()
        # TODO: write some to handle the HTTP headers (they're really important, man)
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


class Restaurant(webapp2.RequestHandler):
    def get(self, restaurant_key):
        # tries to query the Restaurant whose Key is specified in the url path
        # note: the key in url path MUST BE in a urlsafe form
        try:
            restaurant = models.Restaurant.get_restaurants(restaurant_key)
            if restaurant:
                self.response.out.write(json.dumps(restaurant, cls=util.JSONEncoder))
            else:
                self.response.out.write(json.dumps({"msg":"There's no such Restaurant. Try again."}))
        # well, you know...
        # shit happens
        # TODO: write this apart, as a decent error handler
        except Exception, e:
            output = {}
            output["msg"] = "Something went really, really bad. Try again."
            output["error_message"] = e.message
            self.response.out.write(json.dumps(output))

    def delete(self, restaurant_key):
        try:
            models.Restaurant.delete_restaurant(restaurant_key)
            self.response.out.write("Hasta la vista, baby!")
        except Exception, e:
            output = {}
            output["msg"] = "Something went really, really bad. Try again."
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
            output["msg"] = "Something went really, really bad. Try again."
            output["error_message"] = e.message
            self.response.out.write(json.dumps(output))


# it seems that webapp2 doesn't support HTTP method PATCH
# so, the following code monkey patchs the webapp2 to allow it.
# (more information at https://code.google.com/p/webapp-improved/issues/detail?id=69)
allowed_methods = webapp2.WSGIApplication.allowed_methods
new_allowed_methods = allowed_methods.union(('PATCH',))
webapp2.WSGIApplication.allowed_methods = new_allowed_methods

# o index esta num arquivo separado chamado index.html que eh chamado no app.yaml
app = webapp2.WSGIApplication([
    ('/dalton', Project),
    ('/api/restaurant', RestaurantList),
    ('/api/restaurant/([^/]+)', Restaurant)
], debug=True)