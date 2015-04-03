.. contracts-api documentation master file, created by
   sphinx-quickstart on Thu Apr  2 19:48:20 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to contracts-api's documentation!
=========================================

Contents:

.. toctree::
   :maxdepth: 2

Models
======

Models are the core database tables for the contracts api.

.. automodule:: contracts_api.api.models
    :members:

Serializers
===========

Serializers translate the models into actual documents that can be used

.. automodule:: contracts_api.api.serializers
    :members:

Resources
=========

The resources are the core of the API. Right now, the core resources available are ``contracts``, ``flows``, and ``stages``

Contracts
---------

The contract endpoint is at the core of the contracts-api

.. automodule:: contracts_api.api.resources.contracts
    :members:

Stages
------

Stages describe individual points in a contract's lifecycle

.. automodule:: contracts_api.api.resources.stages
    :members:

Flows
-----

Flows describe the various stages that a contract will go through in its lifecycle

.. automodule:: contracts_api.api.resources.flows
    :members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
