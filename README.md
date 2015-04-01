Contracts API
=============

The contracts API provides an interface for managing contracts.

[![Build Status](https://travis-ci.org/codeforamerica/template-maker.svg?branch=master)](https://travis-ci.org/codeforamerica/template-maker)

Contracts API
=============

## What is it?
The contracts API is a Flask app that provides a RESTful API for managing business processes around contracts

#### What's the status?
The contracts API is a in very early stages

## Who made it?
The contract api is a project of the 2015 Pittsburgh Code for America [fellowship team](http://codeforamerica.org/governments/pittsburgh)

## How
#### Core Dependencies
The contracts API is a [Flask](http://flask.pocoo.org/) app. It uses [Postgres](http://www.postgresql.org/) for a database.

It is highly recommended that you use use [virtualenv](https://readthedocs.org/projects/virtualenv/) (and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) for convenience). For a how-to on getting set up, please consult this [howto](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md). It is recommended that you use [postgres.app](http://postgresapp.com/) to handle your Postgres (assuming you are developing on OSX).

#### Install
Use the following commands to bootstrap your environment:

**python app**:

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

As the app expands in functionality, this section will be updated.

#### Testing

The contracts API has no tests at the moment. This section will be filled in later

## License
See [LICENCE.md](https://github.com/codeforamerica/contracts-api/blob/master/LICENCE).
