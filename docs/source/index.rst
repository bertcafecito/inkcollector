.. _topics-index:

==========================
Inkcollector documentation
==========================

Inkcollector is a command-line interface (CLI) tool designed to collect data about the
Disney Lorcana trading card game

.. _getting-help:

Getting help
============

Having trouble? We'd like to help!

* Report bugs with Inkcollector in our `issue tracker`_

.. _issue tracker: https://github.com/bertcafecito/inkcollector/issues

.. _installing-inkcollector:

Installing Inkcollector
=======================

To install Inkcollector, you can use pip:

.. code:: shell

    pip install inkcollector

This will install the latest version of Inkcollector from PyPI.

I strongly recommend that you install Inkcollector in a dedicated virtualenv,
to avoid conflicting with your system packages.

.. _command-line-interface:

Command Line Interface (CLI)
=========================================

The Inkcollector CLI provides access to the Lorecast API for collecting
Lorcana Trading Card Game data, including card sets and individual cards.

Usage
-----

Run the CLI by invoking the main command:

.. code-block:: shell

    python -m inkcollector [OPTIONS] COMMAND [ARGS]...

Main Command
------------

.. code-block:: shell

    python -m inkcollector

Options:
~~~~~~~~

- ``-v``, ``--version``: Display the version of the Inkcollector package.

If no command is provided, the CLI will prompt the user to use ``--help`` for guidance.

Lorcast Group
-------------

This command group is used to collect data from the Lorecast API.

.. code-block:: shell

    python -m inkcollector lorcast COMMAND [ARGS]...

Available Commands:
~~~~~~~~~~~~~~~~~~~

**sets**

Collects all available Lorcana card sets (including promotional sets).

.. code-block:: shell

    python -m inkcollector lorcast sets [OPTIONS]

Options:

- ``-fn``, ``--filename``: Optional filename to save the data.

Behavior:

- Displays how many sets were found.
- Saves the data to a file if a filename is provided.
- Displays an error message if saving fails.

**cards**

Retrieves detailed information about a specific card set.

.. code-block:: shell

    python -m inkcollector lorcast cards --setid <SET_ID> [OPTIONS]

Options:

- ``--setid``: Required. The code or ID of the card set.
- ``-fn``, ``--filename``: Optional filename to save the data.

Behavior:

- Retrieves card details for the specified set.
- Displays the number of cards found.
- Saves the data to a file if a filename is provided.
- Displays an error message if saving fails.

**all**

Fetches and stores all data for sets and their cards.

.. code-block:: shell

    python -m inkcollector lorcast all --outputformat <FORMAT>

Options:

- ``-of``, ``--outputformat``: Required. Currently only supports ``JSON``.

Behavior:

- Fetches all sets.
- Iterates through each set and fetches all associated cards.
- Saves each dataset to individual files in a structured format.

Output Formats
--------------

- Currently, only ``JSON`` is supported for the ``all`` command.

Examples
--------

Check the CLI version:

.. code-block:: shell

    python -m inkcollector --version

Collect sets and save to a file:

.. code-block:: shell

    python -m inkcollector lorcast sets --filename sets.json

Collect cards for a specific set:

.. code-block:: shell

    python -m inkcollector lorcast cards --setid ABC123 --filename cards.json

Collect all sets and their cards:

.. code-block:: shell

    python -m inkcollector lorcast all --outputformat JSON

