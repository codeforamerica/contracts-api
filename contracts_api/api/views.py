# -*- coding: utf-8 -*-

import json
import peewee as pw

from flask import Blueprint, jsonify, abort, request, Response, redirect
from flask.ext.restful import Resource, Api

from contracts_api.database import db
from contracts_api.api.models import Contract, Stage, StageProperty
from contracts_api.api.serializers import ContractSchema, StagePropertySchema, StageSchema
from contracts_api.extensions import rest_api as api

blueprint = Blueprint('api', __name__,
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
                status_comments=data.get('status_comments')
            )

            contract_schema = ContractSchema()

            errors = contract_schema.validate(contract, exclude=('id',))

            if errors:
                response = jsonify(errors)
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
            'contract': ContractSchema(contract).data
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

            valid = ContractSchema(updated, exclude=('id', ))

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
api.add_resource(ContractDetail, '/contract/<int:contract_id>')

class StageList(Resource):
    def get(self):
        stages = (Stage
            .select(Stage, StageProperty)
            .join(StageProperty)
            .order_by(Stage.id)
            .aggregate_rows()
        )

        stage_count = Stage.select().count()

        result = {
            'meta': {
                'page': 1,
                'count': stage_count
            },
            'results': StageSchema(
                stages,
                many=True
            ).data
        }

        return jsonify(result)        

    def post(self):
        '''
        Creates a new stage
        '''
        try:
            with db.transaction() as txn:
                data = json.loads(request.data)

                stage = Stage(
                    name=data.get('name')
                )

                stage_schema = StageSchema(only=('name'))

                stage_errors = stage_schema.validate(stage._data)
                if stage_errors:
                    return jsonify(stage_errors), 400

                stage.save()

                for _property in data.get('properties', []):
                    stage_properties = StageProperty(
                        stage=stage.id,
                        stage_property=_property.get('stage_property')
                    )

                    stage_property_schema = StagePropertySchema(exclude=('id',))

                    stage_property_errors = stage_property_schema.validate(stage_properties._data)

                    if stage_property_errors:
                        txn.rollback()
                        return jsonify(stage_property_errors), 400

                    stage_properties.save()

            db.commit()
            return Response(status=201)

        except pw.IntegrityError:
            txn.rollback()
            return jsonify({'error': 'id already taken'}), 400

        except Exception, e:
            txn.rollback()
            return jsonify({'error': e.message}), 403

class StageDetail(Resource):
    def get(self, stage_id):
        stage = Stage.get(id=stage_id)
        import pdb; pdb.set_trace()

    def put(self, stage_id):
        pass

    def delete(self, stage_id):
        pass

api.add_resource(StageList, '/stages')
api.add_resource(StageDetail, '/stage/<int:stage_id>')
