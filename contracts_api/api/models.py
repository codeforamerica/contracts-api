# -*- coding: utf-8 -*-

from contracts_api.database import BaseModel
import peewee as pw
from playhouse.postgres_ext import ArrayField

class Stage(BaseModel):
    name = pw.CharField()

class StageProperty(BaseModel):
    stage = pw.ForeignKeyField(Stage, related_name='stage_properties', to_field='id')
    stage_property = pw.TextField()

    class Meta:
        db_table = 'stage_property'

class Flow(BaseModel):
    flow_name = pw.CharField(unique=True)
    # because arrays of FKs aren't supported, we will check this on the INSERT side
    stage_order = ArrayField(pw.IntegerField)

class Contract(BaseModel):
    item_number = pw.IntegerField()
    spec_number = pw.CharField()
    department = pw.CharField()
    commodity_title = pw.TextField()
    status_comments = pw.TextField()
    flow_name = pw.ForeignKeyField(Flow, to_field='flow_name', db_column='flow_name')
    current_stage = pw.ForeignKeyField(Stage, related_name='current_stage', db_column='current_stage')

class ContractAudit(BaseModel):
    contract_id = pw.ForeignKeyField(Contract, related_name='contract', to_field='id', db_column='contract_id')
    field_changed = pw.CharField()
    old_value = pw.CharField()
    new_value = pw.CharField()

    class Meta:
        db_table = 'contract_audit'

