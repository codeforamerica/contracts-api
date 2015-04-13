# -*- coding: utf-8 -*-

from marshmallow import Schema, fields, ValidationError
from contracts_api.api.models import Stage, Flow

def validate_not_none(stage_property):
    '''
    Validates if this is not none
    '''
    if stage_property is not None and stage_property != '':
        return True

    raise ValidationError('Stage Property cannot be None or empty')

class StagePropertySchema(Schema):
    '''
    Serialize the properties of an individual stage
    '''
    stage_property = fields.String(required=True, validate=validate_not_none)

    class Meta:
        fields = ('id', 'stage_property')

class StageSchema(Schema):
    '''
    Seralize an individual stage
    '''
    name = fields.String(validate=validate_not_none)
    stage_properties = fields.Nested(StagePropertySchema(exclude=('id', )), many=True)

    class Meta:
        fields = ('id', 'name', 'stage_properties')

def validate_is_stage(input_stage):
    stage = Stage.select().where(Stage.id==int(input_stage.get('id'))).first()

    if stage:
        return True

    raise ValidationError('Not a valid stage')

def validate_is_flow(flow_name):
    flow = Flow.select().where(Flow.flow_name==flow_name).first()

    if flow:
        return True

    raise ValidationError('Not a valid flow name')


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
    flow_name = fields.String(required=True)
    stage_order = fields.List(fields.Integer, required=True, validate=validate_stage_order)

    class Meta:
        fields = ('id', 'flow_name', 'stage_order')

class ContractSchema(Schema):
    '''
    Serialize an individual contract
    '''
    current_stage = fields.Nested(StageSchema(exclude=('stage_properties',)), validate=validate_is_stage)
    flow = fields.Nested(FlowSchema(), validate=validate_is_flow, attribute='flow_name')

    class Meta:
        fields = (
            'id', 'item_number', 'spec_number', 'department',
            'commodity_title', 'status_comments', 'current_stage',
            'flow'
        )
