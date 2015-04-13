# -*- coding: utf-8 -*-
import os

os_env = os.environ

class Config(object):
    SECRET_KEY = os_env.get('CONTRACTS_API_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DATABASE_NAME = os.environ.get('DATABASE_NAME', 'contracts_api')
    DATABASE_USER = os.environ.get('DATABASE_USER', 'bensmithgall')
    DATABASE_HOST = os.environ.get('DATABASE_HOST', 'localhost')

class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar

class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.

class TestConfig(Config):
    '''Testing configuration'''
    ENV = 'test'
    DATABASE_NAME = os.environ.get('DATABASE_NAME', 'contracts_api_test')
    DATABASE_USER = ''
    TESTING = True
    DEBUG = True
