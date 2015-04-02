# -*- coding: utf-8 -*-

from marshmallow import Schema, fields

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
