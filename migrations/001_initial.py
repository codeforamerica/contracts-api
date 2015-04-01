from contracts_api.api.models import Contract

def up():
    Contract.create_table()

def down():
    Contract.drop_table()