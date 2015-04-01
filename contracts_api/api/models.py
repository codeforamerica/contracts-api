# -*- coding: utf-8 -*-

from contracts_api.database import BaseModel
import peewee as pw

class Contract(BaseModel):
    item_number = pw.IntegerField()
    spec_number = pw.CharField()
    department = pw.CharField()
    commodity_title = pw.TextField()
    status_comments = pw.TextField()

