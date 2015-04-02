# -*- coding: utf-8 -*-

import json
import peewee as pw

from flask import Blueprint, jsonify, request, Response
from flask.ext.restful import Resource, Api

from contracts_api.database import db
from contracts_api.api.models import Contract, Stage, StageProperty
from contracts_api.api.serializers import ContractSchema, StagePropertySchema, StageSchema

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
                return errors, 400

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
            return { 'contract': ContractSchema(contract).data }

        return {'error': 'contract not found'}, 404

    def put(self, contract_id):
        try:
            contract = Contract.select().where(Contract.id==contract_id).first()

            if contract:
                data = json.loads(request.data)

                contract = Contract.get(id=contract_id)

                updated = Contract(
                    item_number=data.get('item_number', contract.item_number),
                    spec_number=data.get('spec_number', contract.spec_number),
                    department=data.get('department', contract.department),
                    commodity_title=data.get('commodity_title', contract.commodity_title),
                    status_comments=data.get('status_comments', contract.status_comments)
                )

                contract_schema = ContractSchema(exclude=('id',))
                errors = contract_schema.validate(contract)

                if errors:
                    return errors, 400

                contract.update(**updated._data).execute()
                return Response(status=200)

            return { 'error': 'contract not found' }, 404

        except Exception, e:
            return { 'error': e.message }, 403

    def delete(self, contract_id):
        try:
            Contract.delete().where(Contract.id==contract_id).execute()
            return Response(status=204)
        except Exception, e:
            return { 'error': e.message }, 403

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
        with db.transaction() as txn:
            try:
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
                return {'error': 'id already taken'}, 400

            except Exception, e:
                txn.rollback()
                return {'error': e.message}, 403

class StageDetail(Resource):
    def get(self, stage_id):
        stage = (Stage
            .select(Stage, StageProperty)
            .join(StageProperty)
            .where(Stage.id==stage_id)
            .order_by(Stage.id)
            .aggregate_rows()
        ).first()

        if stage:
            return jsonify({ 'stage': StageSchema(stage).data })

        return {'error': 'stage not found'}, 404

    def put(self, stage_id):
        with db.transaction() as txn:
            try:
                data = json.loads(request.data)

                stage = (Stage.select(Stage, StageProperty)
                    .join(StageProperty)
                    .where(Stage.id==stage_id)
                    .order_by(Stage.id)
                    .aggregate_rows()
                ).first()

                if stage:
                    updated = Stage(
                        name = data.get('name', stage.name)
                    )

                    stage_schema = StageSchema(only=('name',))
                    stage_errors = stage_schema.validate(updated._data)
                    if stage_errors:
                        return stage_errors, 400

                    stage.update(**updated._data).execute()

                    if data.get('properties', None):
                        StageProperty.delete().where(StageProperty.stage==stage_id).execute()

                        for _property in data.get('properties'):
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
                    return Response(status=200)

                return { 'error': 'stage not found' }, 404
            except Exception, e:
                txn.rollback()
                return { 'error': e.message }, 403

    def delete(self, stage_id):
        try:
            stage = (Stage.select(Stage, StageProperty)
                .join(StageProperty)
                .where(Stage.id==stage_id)
                .order_by(Stage.id)
                .aggregate_rows()
            ).first()

            if stage:
                stage.delete_instance(recursive=True)
                return Response(status=204)

            return {'error': 'stage not found'}, 404

        except Exception, e:
            return { 'error': e.message }, 403

api.add_resource(StageList, '/stages')
api.add_resource(StageDetail, '/stage/<int:stage_id>')
