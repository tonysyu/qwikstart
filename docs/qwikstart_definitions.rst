=====================
Qwikstart definitions
=====================

Qwikstart repository types
==========================

Qwikstart repositories can have two parts:
- A qwikstart task specification (typically a `qwikstart.yml` file)
- A repository of files (i.e. directory) used by the task

To support different workflows, this may be structured in a few different ways.

Local repository including task specification
---------------------------------------------

The simplest way to define qwikstart operations is using a local directory containing
a qwikstart task specification. For example, the following is a subset of the examples
directory in this repo:

| ├── examples
| │  ├── copy_file_tree.yml
| │  ├── hello_world
| │  │  └── qwikstart.yml
| │  └── templates
| │     ├── copy-file-tree
| │     │  ├── subdirectory
| │     │  │  └── example-file.txt
| │     │  └── {{ qwikstart.dynamic_directory_name }}
| │     │     └── {{ qwikstart.dynamic_file_name }}.txt

Within this repo, you can run an example by specifying the path to the qwikstart repo:

.. code-block:: bash

    $ qwikstart run examples/copy_file_tree.yml

The `copy_file_tree.yml` is the task specification file and the parent directory is
assumed to be the repository containing files used by the task. For example, templates
used in the copy operation are defined relative to that parent directory:

.. code-block:: yaml

    steps:
        # ... some lines removed
        "Add files from `templates/copy-file-tree`":
            name: add_file_tree
            template_dir: "templates/copy-file-tree"

You can also call `qwikstart run` with a path to a directory, and the task specification
file will be assumed to be `qwikstart.yml` within that directory; for example:

.. code-block:: bash

    $ qwikstart run examples/hello_world


Local task specification with remote repository
-----------------------------------------------

Task specifications can also define a `source.url` parameter that points to a remote
repository. For example, the following example uses a remote
[cookiecutter](https://cookiecutter.readthedocs.io/) repository to retrieve files used
for templating:

.. code-block:: yaml

    source:
        url: "https://github.com/audreyr/cookiecutter-pypackage/"
    steps:
        "Request metadata and configuration":
            name: prompt
            template_variable_prefix: "cookiecutter"
            # ... some lines removed

Within this repo, you can run that example using:

.. code-block:: bash

    $ qwikstart run examples/cookiecutter/audreyr-pypackage.yml


Remote task specification
-------------------------

The same task above can be run as a remote file using the `--repo` option to point to
the git repo and the path to the task specification within the repo:

.. code-block:: bash

    $ qwikstart run --repo https://github.com/tonysyu/qwikstart examples/cookiecutter/audreyr-pypackage.yml

Since that task defines a `source.url` (see previous section), the actual templates used
are completely separate from the task definition file. If `source.url` is not defined,
then the path for source files (e.g. template files) is assumed to be within the repo:

.. code-block:: bash

    $ qwikstart run --repo https://github.com/tonysyu/qwikstart examples/copy_file_tree.yml
