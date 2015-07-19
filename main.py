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


class Project(webapp2.RequestHandler):
    def get(self):
        self.response.write('olars.')


class Restaurant(webapp2.RequestHandler):
    def get(self):
        restaurants = models.Restaurant.get_restaurants()
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
        models.Restaurant.create_restaurant(new)


#o index esta num arquivo separado chamado index.html que eh chamado no app.yaml
app = webapp2.WSGIApplication([
    ('/dalton', Project),
    ('/api/restaurant', Restaurant)
], debug=True)