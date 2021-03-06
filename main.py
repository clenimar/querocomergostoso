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
from api import api, metadata
import webapp2


class Project(webapp2.RequestHandler):
    def get(self):
        self.response.write('olars.')


# o index esta num arquivo separado chamado index.html que eh chamado no app.yaml
app = webapp2.WSGIApplication([
    ('/api/meta/action', metadata.Actions),
    ('/api/meta/todo', metadata.Todos),
    ('/api/restaurant', api.RestaurantList),
    ('/api/restaurant/([^/]+)', api.Restaurant),
    ('/api/restaurant/([^/]+)/order', api.OrderListByRestaurant),
    ('/api/customer/([^/]+)/order', api.OrderListByCustomer),
    ('/api/restaurant/([^/]+)/order/([^/]+)', api.Order),
    ('/api/restaurant/([^/]+)/menu', api.Menu),
    ('/api/restaurant/([^/]+)/menu/([^/]+)', api.ItemMenu),
    ('/api/customer', api.CustomerList),
    ('/api/customer/([^/]+)', api.Customer),
], debug=True)