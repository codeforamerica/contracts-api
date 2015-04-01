# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify
from flask.ext.restful import Resource, Api

blueprint = Blueprint('web', __name__,
        url_prefix='/api/v1'
    )
api = Api(blueprint)

class Contracts(Resource):
    def get(self):
        return jsonify({'test': 'hello'})

api.add_resource(Contracts, '/')