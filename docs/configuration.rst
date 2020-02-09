=============
Configuration
=============

Custom configuration for qwikstart is specified using a yaml file named
`~/.qwikstart/config.yml`. The following sections details expected configuration values:

`repo_cache`
=================

Default:

.. code-block:: yaml

    repo_cache:
        "~/.qwikstart/cached_repos"

Directory where cached qwikstart repos are stored.

`git_abbreviations`
===================

Default:

.. code-block:: yaml

    git_abbreviations:
        gh: "https://github.com/{0}"
        gl: "https://gitlab.com/{0}"
        bb: "https://bitbucket.org/{0}"

Note that custom abbreviations will add/modify this list, so these defaults don't need
to be included with your custom config file.
