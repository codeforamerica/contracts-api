# -*- coding: utf-8 -*-

from flask import Blueprint
from flask.ext.restful import Api

from contracts_api.database import db
from contracts_api.api.resources import (
    ContractList, ContractDetail, StageList, StageDetail
)

blueprint = Blueprint('api', __name__,
        url_prefix='/api/v1'
    )
api = Api(blueprint)

api.add_resource(ContractList, '/contracts')
api.add_resource(ContractDetail, '/contract/<int:contract_id>')

api.add_resource(StageList, '/stages')
api.add_resource(StageDetail, '/stage/<int:stage_id>')
