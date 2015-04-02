# -*- coding: utf-8 -*-

import peewee as pw
from marshmallow import Schema, fields, ValidationError
from contracts_api.api.models import Stage

class ContractSchema(Schema):
    '''
    Serialize an individual contract
    '''
    class Meta:
        fields = ('id', 'item_number', 'spec_number', 'department', 'commodity_title', 'status_comments')

class StagePropertySchema(Schema):
    '''
    Serialize the properties of an individual stage
    '''
    stage_property = fields.String(required=True)

    class Meta:
        fields = ('id', 'stage_property')

class StageSchema(Schema):
    '''
    Seralize an individual stage
    '''
    stage_properties = fields.Nested(StagePropertySchema(exclude=('id', )), many=True)

    class Meta:
        fields = ('id', 'name', 'stage_properties')

def validate_stage_order(input_order):
    # << is a peewee operator for SQL IN
    if len(input_order) == 0:
        raise ValidationError('You must specify at least one stage')

    stages = Stage.select(Stage.id).where(Stage.id << input_order)

    if stages.count() != len(input_order):
        stage_ids = [i.id for i in stages]
        bad_stage_ids = list(set(stage_ids).symmetric_difference(set(input_order)))
        raise ValidationError('The following stage ids do not exist: {stages}'.format(
            stages=', '.join([unicode(i) for i in bad_stage_ids])
        ))

    return True

class FlowSchema(Schema):
    '''
    Serialize an individual flow
    '''
    flow_type = fields.String(required=True)
    stage_order = fields.List(fields.Integer, required=True, validate=validate_stage_order)

    class Meta:
        fields = ('id', 'flow_type', 'stage_order')
