#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import argparse
from arnold import main

from flask.ext.script import Manager, Shell, Server

from contracts_api.app import create_app
from contracts_api.settings import DevConfig, ProdConfig
from contracts_api.database import db

if os.environ.get("CONTRACTS_API_ENV") == 'prod':
    app = create_app(ProdConfig)
else:
    app = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

manager = Manager(app)

def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'User': User}

@manager.command
def migrate_up(fake=False):
    main(
        direction='up',
        database=db,
        directory=os.path.join(HERE, 'migrations'),
        migration_module="migrations",
        fake=fake
    )
    return False

@manager.command
def migrate_down(fake=False):
    main(
        direction='down',
        database=db,
        directory=os.path.join(HERE, 'migrations'),
        migration_module="migrations",
        fake=fake
    )
    return

manager.add_command('server', Server(port=os.environ.get('PORT', 9000)))
manager.add_command('shell', Shell(make_context=_make_context))

if __name__ == '__main__':
    manager.run()
