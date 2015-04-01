# -*- coding: utf-8 -*-

import json
from marshmallow import Serializer, fields

class ContractSerializer(Serializer):
    '''
    Serialize an individual contract
    '''
    class Meta:
        fields = ('id', 'item_number', 'spec_number', 'department', 'commodity_title', 'status_comments')