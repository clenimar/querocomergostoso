#!/usr/bin/env python
import datetime
import json
import models
from google.appengine.ext import ndb

import logging

class JSONEncoder(json.JSONEncoder):
    """ it seems that trying to dump a Query Object after turning it into
        a dict through ndb.Model.to_dict() leads to some annoying errors
        because datetimes are not serializable.

        this encoder overcomes it
        fighting hard as a beast
        our world becomes more pleasant
        until the next bug, at least

        -- clenimar @ 19-07
    """
    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.strftime("%d-%m-%Y")

        elif isinstance(obj, ndb.Key):
            if obj.kind() == "Restaurant":
                return obj.urlsafe()
            elif obj.kind() == "ItemMenu":
                return models.ItemMenu.get_item_menu(obj.urlsafe())
            elif obj.kind() == "Order":
                return models.Order.get_order(obj.urlsafe())

        elif isinstance(obj, ndb.Model):
            d = obj.to_dict()
            if obj.key is not None:
                d['key'] = obj.key.urlsafe()
            return d

        elif isinstance(obj, list):
            pass

        else:
            return json.JSONEncoder.default(self, obj)
