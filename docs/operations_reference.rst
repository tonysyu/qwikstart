====================
Available operations
====================

Qwikstart operations (a.k.a. the steps of a qwikstart task) comprise the core
functionality of qwikstart. Typically, a single operation does something quite simple,
but they are combined to perform more complex tasks. This section summarizes the core
operations available.

See the section on :doc:`./understanding_operations`
for more background on how operations work.

add_file
========

Operation used to add files to a project. This copies a file located in the qwikstart
repository (`template_path`) to a path relative to the working directory
(`target_path`).

Required context
----------------

`target_path`
    File path where rendered template will be saved. This will be relative to
    the current working directory.

`template_path`
    Path to template file relative qwikstart repo directory, which is typically
    the directory containing the `qwikstart.yml` file.

Optional context
----------------

`template_variables`
    |template_variables description|

`template_variable_prefix`
    default: `'qwikstart'`

    |template_variable_prefix description|


add_file_tree
=============

Operation to add a file tree (a.k.a. directory) to a project.

Required context
----------------

`template_dir`
    Path to directory containing template files. This path is relative to the
    qwikstart repo directory, which is typically the directory containing the
    `qwikstart.yml` file.

Optional context
----------------

`target_dir`
    default: Working directory

    Directory where files from `template_dir` will be written. This is relative
    to the current working directory.

`template_variables`
    |template_variables description|

`template_variable_prefix`
    default: `'qwikstart'`

    |template_variable_prefix description|

`ignore`
    List of file patterns to ignore from source directory. Unix-shell-style
    wildcards are accepted. See https://docs.python.org/3/library/fnmatch.html


append_text
===========

Operation for appending text to a given file.

Required context
----------------

`file_path`
    |file_path description|

`text`
    Text that will be appended to `file_path`

Optional context
----------------

`prefix`
    default: `'\n'`

    Text added before appended `text`

`suffix`
    default: `''`

    Text added after appended `text`


define_context
==============

Operation to context variables to the operation context.

Required context
----------------

`context_defs`
    Definition of variables to add to the context. Values can be defined using
    template variables; e.g.::

        context_defs:
            greeting: "Hello {{ qwikstart.name }}!"

Optional context
----------------

`template_variables`
    |template_variables description|

`template_variable_prefix`
    default: `'qwikstart'`

    |template_variable_prefix description|

Output
------

This operation can define arbitrary output values.


echo
====

Operation to echo a message to the console.

Required context
----------------

`message`
    Message displayed to user.

Optional context
----------------

`template_variables`
    |template_variables description|

`template_variable_prefix`
    default: `'qwikstart'`

    |template_variable_prefix description|

`highlight`
    default: `''`

    Name of language used for syntax highlighting using `pygments` library.
    See https://pygments.org/docs/lexers/


edit_json
=========

Operation edit json by merging data into existing json data.

Required context
----------------

`file_path`
    |file_path description|

`merge_data`
    Dictionary of data that will be merged into existing data in json file.

Optional context
----------------

`indent`
    default: 4


edit_yaml
=========

Operation edit yaml by merging data into existing yaml data.

Required context
----------------

`file_path`
    |file_path description|

`merge_data`
    Data that will be merged into existing data in yaml file.


find_files
==========

Operation for searching for text within files and returning file paths.

Optional context
----------------

`regex`
    default: `''`

    Regex to search for in files

`directory`
    default: `'.'`

    Root directory for search (defaults to working directory).

`output_name`
    default: `'matching_files'`

    Variable name where list of matching files is stored.

`path_filter`
    default: `None`

    File filter string passed to `fnmatch` before searching. This can be used
    to speed up searching for large repositories.

    For example, you can limit text search to json files using `"*.json"`.

`regex_flags`
    List of Python regex flags. Any combination of `'IGNORECASE'`, `'MULTILINE'`,
    `'DOTALL'`, `'UNICODE'`. See `docs for Python regex library`_

.. _docs for Python regex library: https://docs.python.org/3/library/re.html

Output
------

This operation can define arbitrary output values.


find_tag_and_insert_text
========================

Operation to find a tag and insert text below that tag.

This is a simple combination of the `find_tagged_line` and `insert_text` operations.


Required context
----------------

`file_path`
    |file_path description|

`tag`
    Text used as a placeholder for detecting where to insert text. For example::

        # qwikstart: inject-line-below

`text`
    Text that will be inserted.

Optional context
----------------

`line_ending`
    default: `'\n'`

    Text appended to the end of inserted text.

`match_indent`
    default: `True`


find_tagged_line
================

Operation inserting text on a given line

Required context

`file_path`
    Path to file relative to the current working directory.

`tag`
    Text used as a placeholder for detecting where to insert text. For example::

        # qwikstart: inject-line-below

Output
------

`line`
    type: <class 'int'>

`column`
    type: <class 'int'>


insert_text
===========

Operation inserting text on a given line

Required context
----------------

`file_path`
    |file_path description|

`text`
    Text that will be inserted.

`line`
    Line number where text will be inserted.

`column`
    Column where the text will be inserted.

Optional context
----------------

`line_ending`
    default: `'\n'`

    Text appended to the end of inserted text.

`match_indent`
    default: `True`


prompt
======

Operation to prompt user for input values.

The input values will be added to a dictionary in the context with a name matching
`output_dict_name`.


Required context
----------------

`inputs`
    List of dictionaries describing prompts for user inputs.
    Each dictionary can have the following keys:

    `name`
        The name of the variable being defined.
    `default`
        Optional default value of variable. Note that this can be defined as
        a template string, with variables defined in previous prompts or from
        template variables in the context
    `help_text`
        Optional info presented to users when responding to prompts.
    `choices`
        A list of allowed choices.

    For example::

        - name: "name"
          default: "World"
        - name: "message"
          default: "Hello {{ qwikstart.name }}!"

Optional context
----------------

`introduction`
    default: `'Please enter the following information:'`

    Message to user before prompting for inputs.

`template_variables`
    |template_variables description|

`template_variable_prefix`
    default: `'qwikstart'`

    |template_variable_prefix description|

Output
------

This operation can define arbitrary output values.


search_and_replace
==================

Operation for searching for text and replacing it with new text.

Required context
----------------

`file_path`
    Path to file relative to the current working directory.

`search`
    Text to search for in file.

`replace`
    Text used to replace text matching `search`.

Optional context
----------------

`use_regex`
    default: `False`

    Use `re.sub` instead of `str.replace`.

shell
=====

Operation to run an arbitrary shell command.

Required context
----------------

`cmd`
    Command or list of command arguments to run.

Optional context
----------------

`echo_output`
    default: `True`

    Toggle display of output to terminal.

`ignore_error_code`
    default: `False`

    Toggle check for error code returned by shell operation.

`output_processor`
    default: `'strip'`

    Processor to run on output `dict_keys(['noop', 'strip'])`

`output_var`
    default: `None`

    Variable name in which output is stored.

`template_variables`
    |template_variables description|

`template_variable_prefix`
    default: `'qwikstart'`

    |template_variable_prefix description|

Output
------

This operation can define arbitrary output values.


.. |file_path description| replace::
    Path to file relative to the current working directory.

.. |template_variable_prefix description| replace::
    Template variables will be nested in this namespace when rendering; e.g:
    `{{<template_variable_prefix>.your_template_variable}}`

.. |template_variables description| replace::
    Dictionary of variables available when rendering the file template.