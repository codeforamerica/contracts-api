#!/usr/bin/env python
# -*- coding: utf-8 -*-

import peewee as pw

db = pw.PostgresqlDatabase(None)

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

def connect_to_database(app):
    '''
    Helper method to connect to database based on app config
    '''
    if app.config.get('ENV') == 'test':
        db.init(app.config.get('DATABASE_NAME'))
    else:
        db.init(app.config.get('DATABASE_NAME'),
            user=app.config.get('DATABASE_USER'),
            host=app.config.get('DATABASE_HOST')
            )
