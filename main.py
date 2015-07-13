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

import models
import webapp2


class Project(webapp2.RequestHandler):
    def get(self):
        self.response.write('olars.')


class Restaurant(webapp2.RequestHandler):
    def get(self):
        try:
            restaurants = models.Restaurant.get_restaurants()
            self.response.headers["Content-Type"] = "application/json"
            self.response.out.write(restaurants)
        except Exception:
            self.error(500)

    def post(self):
        # creates a new Restaurant
        new = models.Restaurant()
        # changes its attributes
        new.email = self.request.get('email')
        new.pwd = self.request.get('password')
        new.name = self.request.get('name')
        new.owner = self.request.get('owner')

        if self.request.get('menu'):
            new.menu = self.request.get('menu')

        # persists the new Restaurant
        models.Restaurant.create_restaurant(new)

        # TODO: return a JSON response


#o index esta num arquivo separado chamado index.html que eh chamado no app.yaml
app = webapp2.WSGIApplication([
    ('/dalton', Project),
    ('/api/restaurant', Restaurant)
], debug=True)


