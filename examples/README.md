qwikstart examples
==================

This directory contains some simple `qwikstart` examples that can be run from
the root directory of this repository.

The following assume you're running examples from an environment with
`qwikstart` installed. If you're running `qwikstart` from a development
environment using `poetry` you should replace `qwikstart` calls with:

    poetry run qwikstart

Hello world
-----------

Running the following should add a simple hello-world text file to the root
directory.

    $ poetry run qwikstart run examples/hello_world.yml
