[![Build Status](https://travis-ci.org/codeforamerica/contracts-api.svg)](https://travis-ci.org/codeforamerica/contracts-api)

Contracts API
=============

## What is it?
The contracts API is a Flask app that provides a RESTful API for managing business processes around contracts

#### What's the status?
The contracts-api is in its very early stages. We are still in the process of figuring out both the structure of the API (what should the endpoints be? How should the underlying data structures fit together?), and the data model (what are the core components of a contract?).

## Who made it?
The contract api is a project of the 2015 Pittsburgh Code for America [fellowship team](http://codeforamerica.org/governments/pittsburgh)

## How
#### Core Dependencies
The contracts API is a [Flask](http://flask.pocoo.org/) app. It uses [Postgres](http://www.postgresql.org/) for a database, and the "Kindergarten stack" of [peewee](http://peewee.readthedocs.org/en/latest/) and [marshmallow](http://marshmallow.readthedocs.org/en/latest/) for ORM and serialization.

It is highly recommended that you use use [virtualenv](https://readthedocs.org/projects/virtualenv/) (and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) for convenience). For a how-to on getting set up, please consult this [howto](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md). It is recommended that you use [postgres.app](http://postgresapp.com/) to handle your Postgres (assuming you are developing on OSX).

#### Install
Use the following commands to bootstrap your environment:

```shell
# clone the repo
git clone https://github.com/codeforamerica/contracts-api
# change into the repo directory
cd contracts-api
# install python dependencies
pip install -r requirements/dev.txt
# bring the database up to speed
python manage.py migrate_up
# run the server
python manage.py server
```

As the app expands in functionality, this section will be updated.

#### Testing

In order to run the tests, you will need to create a test database. You can follow the same procedures outlined in the install section. By default, the database should be named `contracts_api_test`:

```shell
psql
create database test_contracts_api;
```

Tests are located in the `contracts_api_test` directory. To run the tests, run

```shell
PYTHONPATH=. nosetests contracts_api_test/
```

from inside the root directory. For more coverage information, run

```shell
PYTHONPATH=. nosetests contracts_api_test/ -v --with-coverage --cover-package=contracts_api --cover-erase
```

## License
See [LICENCE.md](https://github.com/codeforamerica/contracts-api/blob/master/LICENCE).
