MPTT Demo
=========

MPTT (modified preorder tree traversal) demo.

A simple Categories API that stores category tree to database and returns category parents, children and siblings by category id.

.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


:License: MIT


API
---

**POST /categories/**

.. code-block:: json

  {
    "name": "Category 1",
    "children": [
      {
        "name": "Category 1.1",
        "children": [
          {
            "name": "Category 1.1.1",
            "children": [
              {
                "name": "Category 1.1.1.1"
              },
              {
                "name": "Category 1.1.1.2"
              },
              {
                "name": "Category 1.1.1.3"
              }
            ]
          },
          {
            "name": "Category 1.1.2",
            "children": [
              {
                "name": "Category 1.1.2.1"
              },
              {
                "name": "Category 1.1.2.2"
              },
              {
                "name": "Category 1.1.2.3"
              }
            ]
          }
        ]
      }
    ]
  }


**GET /categories/{ID}**

.. code-block:: json

  {
    "id": 5,
    "name": "Category 1.1.1",
    "parents": [
      {
        "id": 4,
        "name": "Category 1.1"
      },
      {
        "id": 3,
        "name": "Category 2"
      }
    ],
    "children": [
      {
        "id": 6,
        "name": "Category 1.1.1.1"
      },
      {
        "id": 7,
        "name": "Category 1.1.1.2"
      },
      {
        "id": 8,
        "name": "Category 1.1.1.3"
      }
    ],
    "siblings": [
      {
        "id": 9,
        "name": "Category 1.1.2"
      }
    ]
  }

Settings
--------

Create database:

*createdb mptt -U postgres*

Set environment variable:

E.g. *export DATABASE_URL=postgres://postgres:debug@127.0.0.1:5432/mptt*

Basic Commands
--------------

Type checks
^^^^^^^^^^^

Running type checks with mypy:

::

  $ mypy apps

Test coverage
^^^^^^^^^^^^^

To run the tests, check your test coverage, and generate an HTML coverage report::

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

Running tests with py.test
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  $ pytest .
