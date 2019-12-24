=================
Developer's Guide
=================

Prerequisites
=============

The `qwikstart` package uses `poetry <https://github.com/sdispater/poetry>`_ for
dependency management and distribution. You call install `poetry` using::

    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python


Setup
=====

Clone from github::

    git clone https://github.com/tonysyu/qwikstart.git

Install development requirements::

    cd qwikstart
    poetry install

For building the documentation locally, you'll also need to run::

    poetry install --extras "docs"

Development
===========

For local development, you'll also want to install pre-commit hooks using::

    poetry run pre-commit install

By default, this will run the black code formatter on *changed* files on every
commit. To run black on all files::

    poetry run pre-commit run --all-files


Running tests
=============

The test suite can be run without installing dev requirements using::

    $ tox


To run tests with a specific Python version, run::

    $ tox --env py36

You can isolate specific test files/functions/methods with::

    tox PATH/TO/TEST.py
    tox PATH/TO/TEST.py::TEST_FUNCTION
    tox PATH/TO/TEST.py::TEST_CLASS::TEST_METHOD


Documentation
=============

Documentation is built from within the docs directory::

    cd docs
    poetry run make html

After building, you can view the docs at `docs/_build/html/index.html`.


Release
=======

A reminder for the maintainers on how to deploy.

- Update the version and push::

    $ bumpversion patch # possible: major / minor / patch
    $ git push
    $ git push --tags

- Build release and deploy to PyPI::

    $ poetry build
    $ poetry publish
