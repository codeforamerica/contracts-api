#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import peewee as pw

db = pw.PostgresqlDatabase(
    os.environ.get('DATABASE_NAME', 'contracts_api'),
    user=os.environ.get('DATABASE_USER', 'bensmithgall'),
    host=os.environ.get('DATABASE_HOST', 'localhost')
)

class BaseModel(pw.Model):
    """Base Model -- all inheriting classes share the same database"""
    def __marshallable__(self):
        """Return the marshallable dictionary that will be serialized by
        marshmallow. Peewee models have a dictionary representation where the
        ``_data`` key contains all the field:value pairs for the object.
        """
        return dict(self.__dict__)['_data']

    class Meta:
        database = db