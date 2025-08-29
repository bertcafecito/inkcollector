.. _topics-index:

==========================
Inkcollector documentation
==========================

Inkcollector is a command-line interface (CLI) tool designed to collect data about the
Disney Lorcana trading card game. It provides easy access to the Lorcast API for retrieving
card sets, individual card details, and downloading card images.

**Key Features:**

- 🔧 **Configuration File Support**: YAML configuration files for customized workflows
- 📋 **Extraction Profiles**: Predefined and custom profiles for different use cases
- 🏢 **Workspace Management**: Organize outputs across different environments  
- 🎯 **Flexible CLI**: Global options and profile overrides for maximum control
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

.. _configuration-support:

Configuration Support
=====================

Inkcollector v1.1.0+ supports YAML configuration files that allow you to define default settings, 
extraction profiles, and workspace configurations. This makes it easy to customize the tool's 
behavior for different use cases and environments.

Configuration File
------------------

The configuration file is named ``.inkcollector.yaml`` and should be placed in your project directory. 
Inkcollector will automatically search for this file in the current directory and up to 3 parent directories.

Creating a Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Generate a sample configuration file with all default options:

.. code-block:: shell

    inkcollector config init

This creates a ``.inkcollector.yaml`` file with default settings. You can also specify a custom path:

.. code-block:: shell

    inkcollector config init --path my-config.yaml

Configuration Structure
~~~~~~~~~~~~~~~~~~~~~~~

The configuration file has four main sections:

.. code-block:: yaml

    # Default workspace to use when none is specified
    default_workspace: default

    # API configuration
    api_base_url: https://api.lorcast.com
    api_version: v0

    # Extraction profiles define what data to extract and how
    profiles:
      profile-name:
        description: "Profile description"
        extract_data: true      # Whether to extract JSON data
        extract_images: true    # Whether to download images
        image_size: normal      # Image size: small, normal, large
        save_json: true         # Whether to save JSON to files
        print_json: false       # Whether to print JSON to console

    # Workspace configurations define output directories and defaults
    workspaces:
      workspace-name:
        data_output_dir: data
        image_output_dir: images
        default_profile: complete

Extraction Profiles
-------------------

Profiles define what data to extract and how to handle it. Four default profiles are provided:

**Default Profiles:**

1. **complete** - Extract all data and images (default)
   
   - Extracts JSON data and saves to files
   - Downloads images in normal size
   - Does not print to console

2. **images-only** - Extract only card images
   
   - Downloads images in normal size
   - Does not extract or save JSON data

3. **data-only** - Extract only JSON data
   
   - Extracts JSON data and saves to files
   - Does not download images

4. **preview** - Show data in console without saving
   
   - Extracts JSON data and prints to console
   - Does not save files or download images

Workspaces
----------

Workspaces define output directories and default settings for different environments or projects.

The default workspace uses:

- ``data`` directory for JSON files
- ``images`` directory for downloaded images
- ``complete`` profile as default

Configuration Commands
----------------------

Manage your configuration using the ``config`` command:

.. code-block:: shell

    # Show current configuration
    inkcollector config show

    # Show configuration in JSON format
    inkcollector config show --format json

    # List available profiles and workspaces
    inkcollector config list

    # List only profiles
    inkcollector config list --profiles

    # List only workspaces
    inkcollector config list --workspaces

Global Options
--------------

All commands support these global options:

- ``--config PATH``: Specify custom configuration file
- ``--workspace NAME``: Override workspace selection
- ``--profile NAME``: Override profile selection

For detailed configuration examples and advanced usage, see the `Configuration Documentation <CONFIG.md>`_.

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

    inkcollector [GLOBAL_OPTIONS] COMMAND [ARGS]...

Global Options:
~~~~~~~~~~~~~~~

- ``--config PATH``: Specify custom configuration file
- ``--workspace NAME``: Override workspace selection  
- ``--profile NAME``: Override profile selection
- ``-v``, ``--version``: Display the version of the Inkcollector package

Main Command
------------

.. code-block:: shell

    inkcollector

If no command is provided, the CLI will display the help message.

Directory Structure
-------------------

Inkcollector creates directory structure based on your workspace configuration. 
The default workspace creates the following structure in your working directory:

- ``data/``: Contains all downloaded JSON data (configurable via workspace)
  
  - ``data/lorcast/``: Lorcast API data
  - ``data/lorcast/sets.json``: All sets data
  - ``data/lorcast/sets/<set_id>.json``: Individual set card data

- ``images/``: Contains all downloaded card images (configurable via workspace)
  
  - ``images/lorcast/sets/<set_id>/``: Card images organized by set

**Custom Directory Structure:**

You can customize these directories using workspace configurations:

.. code-block:: yaml

    workspaces:
      research:
        data_output_dir: research/data
        image_output_dir: research/images
        default_profile: data-only

This would create:

- ``research/data/``: Custom data directory
- ``research/images/``: Custom images directory

Lorcast Command Group
---------------------

This command group is used to collect data from the Lorcast API. All lorcast commands 
respect configuration profiles and workspace settings.

.. code-block:: shell

    inkcollector [GLOBAL_OPTIONS] lorcast COMMAND [ARGS]...

Available Subcommands:
~~~~~~~~~~~~~~~~~~~~~~

**get-sets**

Collects all available Disney Lorcana card sets from the Lorcast API.

.. code-block:: shell

    inkcollector lorcast get-sets [OPTIONS]

Options:

- ``--json``: Print the JSON data directly to the console with formatted output
- ``--save-json``: Save the data to configured data output directory

Behavior:

- Respects active extraction profile settings
- Fetches all available sets from the Lorcast API
- Displays the number of sets found
- Optionally displays formatted JSON output in the console (based on profile or --json flag)
- Optionally saves data to configured workspace directory (based on profile or --save-json flag)
- Automatically creates necessary directories

**get-cards**

Retrieves detailed card information for a specific set.

.. code-block:: shell

    inkcollector lorcast get-cards --set-id <SET_ID> [OPTIONS]

Required Arguments:

- ``--set-id``: The ID of the card set to retrieve cards from

Options:

- ``--json``: Print the JSON card data directly to the console with formatted output
- ``--save-json``: Save the card data to configured data output directory
- ``--get-images [SIZE]``: Download card images with specified size

  - Available sizes: ``small``, ``normal``, ``large``
  - Default size: ``normal`` (if no size specified)
  - Images saved to configured image output directory

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

**Configuration Management:**

Check the CLI version:

.. code-block:: shell

    inkcollector --version

Create a configuration file:

.. code-block:: shell

    inkcollector config init

Show current configuration:

.. code-block:: shell

    inkcollector config show

List available profiles and workspaces:

.. code-block:: shell

    inkcollector config list

**Using Profiles:**

Use preview profile (console output only):

.. code-block:: shell

    inkcollector --profile preview lorcast get-sets

Use images-only profile:

.. code-block:: shell

    inkcollector --profile images-only lorcast get-cards --set-id TFC

Use custom workspace:

.. code-block:: shell

    inkcollector --workspace research lorcast get-sets

**Legacy CLI Usage:**

Display help for the main command:

.. code-block:: shell

    inkcollector --help

Display help for lorcast commands:

.. code-block:: shell

    inkcollector lorcast --help

Fetch all sets and display JSON in console:

.. code-block:: shell

    inkcollector lorcast get-sets --json

Fetch all sets and save to file:

.. code-block:: shell

    inkcollector lorcast get-sets --save-json

Fetch all sets, display in console, and save to file:

.. code-block:: shell

    inkcollector lorcast get-sets --json --save-json

Fetch cards for a specific set and display in console:

.. code-block:: shell

    inkcollector lorcast get-cards --set-id TFC --json

Fetch cards for a specific set and save to file:

.. code-block:: shell

    inkcollector lorcast get-cards --set-id TFC --save-json

Download normal-sized card images for a set:

.. code-block:: shell

    inkcollector lorcast get-cards --set-id TFC --get-images

Download large-sized card images for a set:

.. code-block:: shell

    inkcollector lorcast get-cards --set-id TFC --get-images large

Fetch cards, save data, and download images in one command:

.. code-block:: shell

    inkcollector lorcast get-cards --set-id TFC --json --save-json --get-images normal

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

- ``requests>=2.32.3``: HTTP client for API communication
- ``PyYAML>=6.0``: YAML configuration file support
- ``argparse``: Command-line argument parsing
- ``json``: JSON data handling
- ``os``: File system operations
