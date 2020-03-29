qwikstart: Code generator for fun and profit
============================================

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

`qwikstart` is a code generator for integrating code into existing projects. It's
similar to code generators like cookiecutter_, yeoman_, and hygen_ but with a focus on
adding code to existing projects.

A simple `hello-world.yml` script in qwikstart would look something like:

.. code-block:: yaml

    steps:
        "Ask for name":
            name: prompt
            inputs:
                - name: "name"
                  default: "World"
        "Display message":
            name: echo
            message: |

                Hello, {{ qwikstart.name }}!

The first step uses the `prompt` operation with a single input `"name"`, with a default
value of `"World"` (which is editable when running the script). The next step just uses
the `echo` operation to display a message. This script can be using `qwikstart run`:

.. code-block:: bash

    $ qwikstart run hello-world.yml

    Please enter the following information:
    name: World

    Hello, World!

Install
=======

The recommended way of installing `qwikstart` is to use pipx_:

.. code-block:: bash

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

After installing `qwikstart`, you can run a simple hello-world example using the
following:

.. code-block:: bash

    $ qwikstart run --repo https://github.com/tonysyu/qwikstart examples/hello_world.yml


By default, there are abbreviations for common git repos, so the above can also be
written:

.. code-block:: bash

    qwikstart run --repo gh:tonysyu/qwikstart examples/hello_world.yml


See Also
========

There are a lot code generators and scaffolding tools out there, and the following is
just a selection of some of the most popular ones:

- cookiecutter_: A command-line utility that creates projects from cookiecutters
  (project templates)
- hygen_: The scalable code generator that saves you time.
- yeoman_: The web's scaffolding tool for modern webapps

.. _hygen: https://www.hygen.io/
.. _cookiecutter: https://cookiecutter.readthedocs.io/
.. _yeoman: https://yeoman.io/

