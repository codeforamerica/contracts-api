from flask.ext.testing import TestCase

from contracts_api.settings import TestConfig
from contracts_api.app import create_app as _create_app
from contracts_api.database import db
from contracts_api.api.models import Stage, Contract, StageProperty, ContractAudit, Flow

class BaseTestCase(TestCase):
    '''
    A base test case that boots our app
    '''
    def create_app(self):
        return _create_app(TestConfig)

    def setUp(self):
        db.connect()
        db.create_tables([Stage, Contract, StageProperty, ContractAudit, Flow])

    def tearDown(self):
        db.connect()
        db.drop_tables([Stage, Contract, StageProperty, ContractAudit, Flow])
        db.close()
