from contracts_api.database import db
from contracts_api.api.models import Contract, Stage, StageProperty, ContractAudit, Flow

def up():
    db.connect()

    db.create_tables([Stage, Contract, StageProperty, ContractAudit, Flow])

def down():
    db.connect()

    db.drop_tables([Stage, Contract, StageProperty, ContractAudit, Flow])
