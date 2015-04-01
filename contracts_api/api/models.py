# -*- coding: utf-8 -*-

from contracts_api.database import BaseModel
import peewee as pw
from playhouse.postgres_ext import ArrayField

class Stage(BaseModel):
    name = pw.CharField()

class StageProperty(BaseModel):
    stage_id = pw.ForeignKeyField(Stage, related_name='stage', to_field='id')
    stage_property = pw.TextField()

    class Meta:
        db_table = 'stage_property'

class Contract(BaseModel):
    item_number = pw.IntegerField()
    spec_number = pw.CharField()
    department = pw.CharField()
    commodity_title = pw.TextField()
    status_comments = pw.TextField()
    current_stage = pw.ForeignKeyField(Stage, to_field='id')

class ContractAudit(BaseModel):
    contract_id = pw.ForeignKeyField(Contract, related_name='contract', to_field='id')
    field_changed = pw.CharField()
    old_value = pw.CharField()
    new_value = pw.CharField()

    class Meta:
        db_table = 'contract_audit'

class Flow(BaseModel):
    flow_type = pw.CharField()
    # because arrays of FKs aren't supported, we will check this on the INSERT side
    stage_order = ArrayField(pw.IntegerField)

