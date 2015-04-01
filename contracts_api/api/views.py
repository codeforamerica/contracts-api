# -*- coding: utf-8 -*-

import json
import peewee as pw

from flask import Blueprint, jsonify, abort, request, Response
from flask.ext.restful import Resource, Api
from contracts_api.api.models import Contract
from contracts_api.api.serializers import ContractSerializer

blueprint = Blueprint('web', __name__,
        url_prefix='/api/v1'
    )
api = Api(blueprint)

class ContractList(Resource):
    def get(self):
        contracts = Contract.select()
        contract_count = contracts.count()

        result = {
            'meta': {
                'page': 1,
                'count': contract_count
            },
            'results': ContractSerializer(
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
                status_comments=data.get('status_comments')
            )

            valid = ContractSerializer(contract, exclude=('id',))

            if not valid.is_valid():
                response = jsonify(valid.errors)
                response.status_code = 400
                return response

            contract.save()
            return Response(status=201)

        except pw.IntegrityError, e:
            response = jsonify({'error': e.message})
            response.status_code = 400
            return response

        except Exception, e:
            repsonse = jsonify({'error': e.message})
            response.status_code = 403
            return response

class ContractDetail(Resource):
    def get(self, contract_id):
        contract = Contract.get(id=contract_id)

        return jsonify({
            'contract': ContractSerializer(contract).data
        })

    def put(self, contract_id):
        try:
            data = json.loads(request.data)

            contract = Contract.get(id=contract_id)

            updated = Contract(
                item_number=data.get('item_number', contract.item_number),
                spec_number=data.get('spec_number', contract.spec_number),
                department=data.get('department', contract.department),
                commodity_title=data.get('commodity_title', contract.commodity_title),
                status_comments=data.get('status_comments', contract.status_comments)
            )

            valid = ContractSerializer(updated, exclude=('id', ))

            if not valid.is_valid():
                response = jsonify(valid.errors)
                response.status_code = 400
                return response

            contract.update(**updated._data).execute()
            return Response(status=200)

        except Exception, e:
            response = jsonify({'error': e.message})
            response.status_code = 403
            return response

    def delete(self, contract_id):
        try:
            Contract.delete().where(Contract.id==contract_id).execute()
            return Response(status=204)
        except Exception, e:
            response = jsonify({'error': e.message})
            response.status_code = 403
            return response

api.add_resource(ContractList, '/contracts')
api.add_resource(ContractDetail, '/contracts/<int:contract_id>')
