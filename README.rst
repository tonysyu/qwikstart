qwikstart: Code injector for fun and profit
===========================================

.. default-role:: literal

.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://github.com/tonysyu/qwikstart/blob/master/LICENSE

.. image:: https://travis-ci.com/tonysyu/qwikstart.svg?branch=master
   :target: https://travis-ci.com/tonysyu/qwikstart

.. image:: https://codecov.io/gh/tonysyu/qwikstart/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/tonysyu/qwikstart

.. image:: https://readthedocs.org/projects/qwikstart/badge/
   :target: https://qwikstart.readthedocs.io


- **Documentation:** https://qwikstart.readthedocs.io
- **Source:** https://github.com/tonysyu/qwikstart

Install
=======

The recommended way of installing `qwikstart` is to use pipx_::

    pipx install qwikstart

If you happen to be setting up pipx_ for the first time, the
`pipx installation instructions`_ suggest running `pipx ensurepath` to update
the user path. Note, if you use `~/.profile` instead of `~/.bash_profile`,
this will add `~/.bash_profile`, which will take precendence over `~/.profile`.
Either move the code from `~/.bash_profile` to `~/.profile` or
`link your profiles <https://superuser.com/a/789465>`_.

.. _pipx: https://pypi.org/project/pipx/
.. _pipx installation instructions:
    https://pipxproject.github.io/pipx/installation/

Basic Usage
===========

After installing `qwikstart`, you can run a simple hello-world example using the following::

    qwikstart run --repo https://github.com/tonysyu/qwikstart examples/hello_world.yml

By default, there are abbreviations for common git repos, so the above can also be written::

    qwikstart run --repo gh:tonysyu/qwikstart examples/hello_world.yml


See Also
========

- `hygen <https://www.hygen.io/>`_: The scalable code generator that saves you
  time.
- `cookiecutter <https://cookiecutter.readthedocs.io/>`_:
  A command-line utility that creates projects from cookiecutters (project
  templates)
- `pyscaffold <https://pyscaffold.org/>`_: Python project template generator
  with batteries included.
