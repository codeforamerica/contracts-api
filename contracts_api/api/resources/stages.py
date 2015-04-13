import json
import peewee as pw

from flask import jsonify, request, Response
from flask.ext.restful import Resource

from contracts_api.database import db
from contracts_api.api.models import Stage, StageProperty
from contracts_api.api.serializers import StagePropertySchema, StageSchema

class StageList(Resource):
    def get(self):
        stages = (Stage
            .select(Stage, StageProperty)
            .join(StageProperty, join_type=pw.JOIN_LEFT_OUTER)
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
                    return stage_errors, 400

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
                        return stage_property_errors, 400

                    stage_properties.save()

                db.commit()
                return Response(status=201)

            except pw.IntegrityError:
                txn.rollback()
                return {'error': 'id already taken'}, 403

            except Exception, e:
                txn.rollback()
                return {'error': e.message}, 403

class StageDetail(Resource):
    def get(self, stage_id):
        stage = (Stage
            .select(Stage, StageProperty)
            .join(StageProperty, join_type=pw.JOIN_LEFT_OUTER)
            .where(Stage.id==stage_id)
            .order_by(Stage.id)
            .aggregate_rows()
        ).first()

        if stage:
            return StageSchema(stage).data

        return {'error': 'stage not found'}, 404

    def put(self, stage_id):
        with db.transaction() as txn:
            try:
                data = json.loads(request.data)

                stage = (Stage.select(Stage, StageProperty)
                    .join(StageProperty, join_type=pw.JOIN_LEFT_OUTER)
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
                                return stage_property_errors, 400

                            stage_properties.save()

                    db.commit()
                    return Response(status=200)

                return { 'error': 'stage not found' }, 404
            except Exception, e:
                txn.rollback()
                return { 'error': e.message }, 403

    def delete(self, stage_id):
        stage = (Stage.select(Stage, StageProperty)
            .join(StageProperty, join_type=pw.JOIN_LEFT_OUTER)
            .where(Stage.id==stage_id)
            .order_by(Stage.id)
            .aggregate_rows()
        ).first()

        if stage:
            stage.delete_instance(recursive=True)
            return Response(status=204)

        return {'error': 'stage not found'}, 404
