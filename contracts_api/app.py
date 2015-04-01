# -*- coding: utf-8 -*-
'''The app module, containing the app factory function.'''
from flask import Flask, render_template

from contracts_api.settings import DevConfig, ProdConfig
from contracts_api.extensions import (
    debug_toolbar
)
from contracts_api import api


def create_app(config_object=DevConfig):
    '''An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    '''
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    return app

def register_extensions(app):
    debug_toolbar.init_app(app)
    return None

def register_blueprints(app):
    app.register_blueprint(api.views.blueprint)
    return None
