#!/usr/bin/env python
import json
import util
import webapp2
from google.appengine.ext import ndb


class Action(ndb.Model):
    desc = ndb.StringProperty()
    author = ndb.StringProperty()


class Todo(ndb.Model):
    desc = ndb.StringProperty()


class Actions(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(json.dumps(Action.query().fetch(20), cls=util.JSONEncoder))

    def post(self):
        data = json.loads(self.request.body)
        if "desc" not in data.keys() or "author" not in data.keys(): webapp2.abort(400)
        new = Action()
        new.desc = data['desc']
        new.author = data['author']
        new.put()
        self.response.out.write(json.dumps({"message":"Are you working? Really? Great!"}))


class Todos(webapp2.RequestHandler):
    def get(self):
        self.response.out.write(json.dumps(Todo.query().fetch(20), cls=util.JSONEncoder))

    def post(self):
        data = json.loads(self.request.body)
        if "desc" not in data.keys(): webapp2.abort(400)
        new = Todo()
        new.desc = data["desc"]
        new.put()
        self.response.out.write(json.dumps({"message":"Okay, task registered. Time to work, huh?"}))