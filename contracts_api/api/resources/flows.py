# -*- coding: utf-8 -*-

import json
import peewee as pw

from flask import jsonify, request, Response
from flask.ext.restful import Resource

from contracts_api.api.models import Flow
from contracts_api.api.serializers import FlowSchema

class FlowList(Resource):
    def get(self):
        flows = Flow.select()
        flow_count = flows.count()

        result = {
            'meta': {
                'page': 1,
                'count': flow_count
            },
            'results': FlowSchema(
                flows,
                many=True
            ).data
        }

        return jsonify(result)

    def post(self):
        try:
            data = json.loads(request.data)


            flow = Flow(
                flow_type = data.get('flow_type'),
                stage_order = data.get('stage_order')
            )

            flow_schema = FlowSchema(exclude=('id',))
            errors = flow_schema.validate(flow._data)
            if errors:
                return errors, 400

            flow.save()
            return Response(status=201)

        except pw.IntegrityError, e:
            return { 'error': e.message }, 400

        except Exception, e:
            return { 'error': e.message }, 403

class FlowDetail(Resource):
    def get(self, flow_id):
        flow = Flow.select().where(Flow.id==flow_id).first()

        if flow:
            return { 'flow': FlowSchema(flow).data }

        return { 'error': 'flow not found' }, 404

    def put(self, flow_id):
        try:
            flow = Flow.select().where(Flow.id==flow_id).first()

            if flow:
                data = json.loads(request.data)

                updated = Flow(
                    flow_type = data.get('flow_type', flow.flow_type),
                    stage_order = data.get('stage_order', flow.stage_order)
                )

                flow_schema = FlowSchema(exclude=('id',))
                errors = flow_schema.validate(updated._data)
                if errors:
                    return errors, 400

                flow.update(**updated._data).execute()
                return Response(status=200)

            return { 'error': 'flow not found' }, 404
        except Exception, e:
            return { 'error': e.message }, 403

    def delete(self, flow_id):
        try:
            flow = Flow.select().where(Flow.id==flow_id).first()

            if flow:
                flow.delete_instance()
                return Response(status=204)

            return { 'error': 'flow not found' }, 404
        except Exception, e:
            return { 'error': e.message }, 403

