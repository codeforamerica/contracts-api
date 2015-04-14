# -*- coding: utf-8 -*-

import json
import peewee as pw

from flask import jsonify, Response, request
from flask.ext.restful import Resource

from contracts_api.api.models import Contract
from contracts_api.api.serializers import ContractSchema

class ContractList(Resource):
    def get(self):
        contracts = Contract.select()
        contract_count = contracts.count()

        result = {
            'meta': {
                'page': 1,
                'count': contract_count
            },
            'results': ContractSchema(
                contracts,
                many=True
            ).data
        }

        return jsonify(result)

    def post(self):
        try:
            data = json.loads(request.data)

            contract = Contract(
                item_number=data.get('item_number'),
                spec_number=data.get('spec_number', None),
                department=data.get('department', None),
                commodity_title=data.get('commodity_title', None),
                status_comments=data.get('status_comments'),
                current_stage=dict(id=data.get('current_stage')),
                flow_name=dict(flow_name=data.get('flow_name'))
            )

            contract_schema = ContractSchema(exclude=('id',))
            errors = contract_schema.validate(contract._data)

            if errors:
                return errors, 400
            else:
                contract.current_stage = data.get('current_stage')
                contract.flow_name = data.get('flow_name')

            contract.save()
            return Response(status=201)

        except pw.IntegrityError, e:
            return { 'error': e.message }, 400

        except Exception, e:
            return { 'error': e.message }, 403

class ContractDetail(Resource):
    def get(self, contract_id):
        contract = Contract.select().where(Contract.id==contract_id).first()

        if contract:
            return ContractSchema(contract).data

        return {'error': 'contract not found'}, 404

    def put(self, contract_id):
        try:
            contract = Contract.select().where(Contract.id==contract_id).first()

            if contract:
                data = json.loads(request.data)

                updated = Contract(
                    item_number=data.get('item_number', contract.item_number),
                    spec_number=data.get('spec_number', contract.spec_number),
                    department=data.get('department', contract.department),
                    commodity_title=data.get('commodity_title', contract.commodity_title),
                    status_comments=data.get('status_comments', contract.status_comments),
                    current_stage=dict(id=data.get('current_stage', contract.current_stage)),
                    flow_name=dict(flow_name=data.get('flow_name', contract.flow_name.flow_name))
                )

                contract_schema = ContractSchema(exclude=('id',))
                errors = contract_schema.validate(updated._data)

                if errors:
                    return errors, 400
                else:
                    updated.current_stage = data.get('current_stage', contract.current_stage)
                    updated.flow_name = data.get('flow_name', contract.flow_name.flow_name)

                contract.update(**updated._data).execute()
                return Response(status=200)

            return { 'error': 'contract not found' }, 404

        except Exception, e:
            return { 'error': e.message }, 403

    def delete(self, contract_id):
        contract = Contract.select().where(Contract.id==contract_id).first()

        if contract:
            contract.delete().execute()
            return Response(status=204)
        else:
            return { 'error': 'contract not found' }, 404
