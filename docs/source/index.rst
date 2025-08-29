.. _topics-index:

==========================
Inkcollector documentation
==========================

Inkcollector is a command-line interface (CLI) tool designed to collect data about the
Disney Lorcana trading card game. It provides easy access to the Lorcast API for retrieving
card sets, individual card details, and downloading card images.

**Key Features:**

- Fetch all available Disney Lorcana card sets
- Retrieve detailed card information for specific sets
- Download card images in multiple sizes (small, normal, large)
- Automatic file organization and directory structure creation
- JSON data export with console display options
- Comprehensive error handling and user feedback

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

The Inkcollector CLI provides access to the Lorcast API for collecting
Disney Lorcana Trading Card Game data, including card sets, individual cards,
and card images.

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

If no command is provided, the CLI will display the help message.

Directory Structure
-------------------

Inkcollector automatically creates the following directory structure in your working directory:

- ``data/``: Contains all downloaded JSON data
  
  - ``data/lorcast/``: Lorcast API data
  - ``data/lorcast/sets.json``: All sets data
  - ``data/lorcast/sets/<set_id>.json``: Individual set card data

- ``images/``: Contains all downloaded card images
  
  - ``images/lorcast/sets/<set_id>/``: Card images organized by set

Lorcast Command Group
---------------------

This command group is used to collect data from the Lorcast API.

.. code-block:: shell

    python -m inkcollector lorcast COMMAND [ARGS]...

Available Subcommands:
~~~~~~~~~~~~~~~~~~~~~~

**get-sets**

Collects all available Disney Lorcana card sets from the Lorcast API.

.. code-block:: shell

    python -m inkcollector lorcast get-sets [OPTIONS]

Options:

- ``--json``: Print the JSON data directly to the console with formatted output
- ``--save-json``: Save the data to ``data/lorcast/sets.json``

Behavior:

- Fetches all available sets from the Lorcast API
- Displays the number of sets found
- Optionally displays formatted JSON output in the console
- Optionally saves data to a structured file path
- Automatically creates necessary directories

**get-cards**

Retrieves detailed card information for a specific set.

.. code-block:: shell

    python -m inkcollector lorcast get-cards --set-id <SET_ID> [OPTIONS]

Required Arguments:

- ``--set-id``: The ID of the card set to retrieve cards from

Options:

- ``--json``: Print the JSON card data directly to the console with formatted output
- ``--save-json``: Save the card data to ``data/lorcast/sets/<set_id>.json``
- ``--get-images [SIZE]``: Download card images with specified size

  - Available sizes: ``small``, ``normal``, ``large``
  - Default size: ``normal`` (if no size specified)
  - Images saved to: ``images/lorcast/sets/<set_id>/crd_<card_id>.jpg``

Behavior:

- Validates the set ID by fetching set information first
- Retrieves all cards for the specified set
- Displays the number of cards found
- Optionally displays formatted JSON output in the console
- Optionally saves card data to a structured file path
- Optionally downloads card images in the specified size
- Reports download success/failure statistics for images
- Automatically creates necessary directories

Image Download Features
-----------------------

The CLI supports downloading card images in three sizes:

- **small**: Thumbnail-sized images for quick previews
- **normal**: Standard resolution images (default)
- **large**: High-resolution images for detailed viewing

Image files are automatically named using the pattern ``crd_<card_id>.jpg`` and organized by set in the ``images/lorcast/sets/<set_id>/`` directory.

Error Handling
--------------

The CLI includes comprehensive error handling for:

- Network connection failures
- API timeout errors
- Invalid set IDs
- Missing image URIs
- File system errors
- JSON parsing errors

Output Examples
---------------

When fetching sets with console output:

.. code-block:: text

    ============================================================
                        DISNEY LORCANA SETS                   
    ============================================================
    Found 5 sets:

    [JSON data displayed here]

When fetching cards with console output:

.. code-block:: text

    ============================================================
                        DISNEY LORCANA CARDS                  
    ============================================================
    Found 204 cards in set TFC:

    [JSON data displayed here]

When downloading images:

.. code-block:: text

    Downloading images for 204 cards...
    Successfully downloaded 201 out of 204 card images.

Examples
--------

Check the CLI version:

.. code-block:: shell

    python -m inkcollector --version

Display help for the main command:

.. code-block:: shell

    python -m inkcollector --help

Display help for lorcast commands:

.. code-block:: shell

    python -m inkcollector lorcast --help

Fetch all sets and display JSON in console:

.. code-block:: shell

    python -m inkcollector lorcast get-sets --json

Fetch all sets and save to file:

.. code-block:: shell

    python -m inkcollector lorcast get-sets --save-json

Fetch all sets, display in console, and save to file:

.. code-block:: shell

    python -m inkcollector lorcast get-sets --json --save-json

Fetch cards for a specific set and display in console:

.. code-block:: shell

    python -m inkcollector lorcast get-cards --set-id TFC --json

Fetch cards for a specific set and save to file:

.. code-block:: shell

    python -m inkcollector lorcast get-cards --set-id TFC --save-json

Download normal-sized card images for a set:

.. code-block:: shell

    python -m inkcollector lorcast get-cards --set-id TFC --get-images

Download large-sized card images for a set:

.. code-block:: shell

    python -m inkcollector lorcast get-cards --set-id TFC --get-images large

Fetch cards, save data, and download images in one command:

.. code-block:: shell

    python -m inkcollector lorcast get-cards --set-id TFC --json --save-json --get-images normal

API Integration
===============

Lorcast API
-----------

Inkcollector integrates with the Lorcast API (https://api.lorcast.com/v0) to provide access to Disney Lorcana trading card data.

**Supported Endpoints:**

- ``/sets``: Retrieves all available card sets
- ``/sets/{set_id}``: Gets detailed information about a specific set
- ``/sets/{set_id}/cards``: Retrieves all cards for a specific set

**Data Structure:**

The API returns JSON data with the following structure for sets:

.. code-block:: json

    {
      "results": [
        {
          "id": "TFC",
          "name": "The First Chapter",
          "code": "TFC",
          "released_at": "2023-08-18",
          "card_count": 204
        }
      ]
    }

For cards, each card object includes:

- Basic information (id, name, type, cost, etc.)
- Game mechanics (abilities, keywords, characteristics)
- Image URIs in multiple sizes and formats
- Set and rarity information

Technical Implementation
========================

**Class Structure:**

- ``InkcollectorCLI``: Main CLI handler with argument parsing and command routing
- ``LorcastAPI``: API client for Lorcast service integration

**Dependencies:**

- ``requests``: HTTP client for API communication
- ``argparse``: Command-line argument parsing
- ``json``: JSON data handling
- ``os``: File system operations
