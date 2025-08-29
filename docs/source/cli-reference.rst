.. _cli-reference:

=============
CLI Reference
=============

Complete reference for all Inkcollector commands and options.

Global Options
==============

These options can be used with any command:

.. option:: --config PATH

   Specify custom configuration file path.
   
   **Default:** Search for ``.inkcollector.yaml`` in current and parent directories
   
   **Example:** ``inkcollector --config my-config.yaml lorcast get-sets``

.. option:: --workspace NAME

   Override workspace selection.
   
   **Default:** Uses ``default_workspace`` from configuration
   
   **Example:** ``inkcollector --workspace research lorcast get-sets``

.. option:: --profile NAME

   Override profile selection.
   
   **Default:** Uses workspace's ``default_profile``
   
   **Example:** ``inkcollector --profile preview lorcast get-sets``

.. option:: --output-dir PATH

   Override default data output directory.
   
   **Behavior:** Provides complete path control, bypassing default ``lorcast/`` subdirectory structure
   
   **Default:** Uses workspace's ``data_output_dir`` with ``lorcast/`` subdirectories
   
   **Example:** ``inkcollector --output-dir /custom/data lorcast get-sets``

.. option:: --image-dir PATH

   Override default image output directory.
   
   **Behavior:** Provides complete path control, bypassing default ``lorcast/sets/{set-id}/`` subdirectory structure
   
   **Default:** Uses workspace's ``image_output_dir`` with ``lorcast/sets/{set-id}/`` subdirectories
   
   **Example:** ``inkcollector --image-dir /custom/images lorcast get-cards --set-id TFC --get-images``

.. option:: -v, --version

   Display the version of Inkcollector.
   
   **Example:** ``inkcollector --version``

.. option:: --help

   Show help message and exit.

Main Commands
=============

inkcollector
------------

Main entry point for all commands.

**Syntax:**

.. code-block:: shell

    inkcollector [GLOBAL_OPTIONS] COMMAND [ARGS]...

**Examples:**

.. code-block:: shell

    # Show help
    inkcollector --help
    
    # Show version
    inkcollector --version
    
    # Use with global options
    inkcollector --config my-config.yaml --workspace dev lorcast get-sets
    
    # Custom output directories
    inkcollector --output-dir /project/data --image-dir /project/images lorcast get-cards --set-id TFC --save-json --get-images

Configuration Commands
=====================

config
------

Manage configuration files and settings.

**Syntax:**

.. code-block:: shell

    inkcollector config SUBCOMMAND [OPTIONS]

config init
~~~~~~~~~~~

Create a new configuration file with default settings.

**Syntax:**

.. code-block:: shell

    inkcollector config init [OPTIONS]

**Options:**

.. option:: --path PATH

   Specify where to create the configuration file.
   
   **Default:** ``.inkcollector.yaml`` in current directory

**Examples:**

.. code-block:: shell

    # Create default config
    inkcollector config init
    
    # Create at specific path
    inkcollector config init --path projects/my-config.yaml

config show
~~~~~~~~~~~

Display current configuration settings.

**Syntax:**

.. code-block:: shell

    inkcollector config show [OPTIONS]

**Options:**

.. option:: --format FORMAT

   Output format for configuration display.
   
   **Choices:** ``yaml``, ``json``
   
   **Default:** ``yaml``

**Examples:**

.. code-block:: shell

    # Show in YAML format (default)
    inkcollector config show
    
    # Show in JSON format
    inkcollector config show --format json

config list
~~~~~~~~~~~

List available profiles and workspaces.

**Syntax:**

.. code-block:: shell

    inkcollector config list [OPTIONS]

**Options:**

.. option:: --profiles

   Show only profiles.

.. option:: --workspaces

   Show only workspaces.

**Examples:**

.. code-block:: shell

    # List everything
    inkcollector config list
    
    # List only profiles
    inkcollector config list --profiles
    
    # List only workspaces
    inkcollector config list --workspaces

Lorcast Commands
===============

lorcast
-------

Access Disney Lorcana data from the Lorcast API.

**Syntax:**

.. code-block:: shell

    inkcollector [GLOBAL_OPTIONS] lorcast COMMAND [ARGS]...

**Examples:**

.. code-block:: shell

    # Show lorcast help
    inkcollector lorcast --help

lorcast get-sets
~~~~~~~~~~~~~~~~

Retrieve all available Disney Lorcana card sets.

**Syntax:**

.. code-block:: shell

    inkcollector lorcast get-sets [OPTIONS]

**Options:**

.. option:: --json

   Print JSON data to console with formatted output.
   
   **Note:** Overrides profile's ``print_json`` setting.

.. option:: --save-json

   Save JSON data to configured data output directory.
   
   **Note:** Overrides profile's ``save_json`` setting.

**Behavior:**

- Respects active extraction profile settings
- Fetches all available sets from Lorcast API
- Displays number of sets found
- Creates necessary directories automatically
- **Default mode:** Saves to ``{data_output_dir}/lorcast/sets.json``
- **Custom directory mode:** When ``--output-dir`` is used, saves directly to ``{output_dir}/sets.json`` (bypasses ``lorcast/`` subdirectory)

**Examples:**

.. code-block:: shell

    # Use profile defaults
    inkcollector lorcast get-sets
    
    # Print to console
    inkcollector lorcast get-sets --json
    
    # Save to file
    inkcollector lorcast get-sets --save-json
    
    # Both print and save
    inkcollector lorcast get-sets --json --save-json
    
    # With custom profile
    inkcollector --profile preview lorcast get-sets
    
    # Save to custom directory (full override)
    inkcollector --output-dir /my/custom/path lorcast get-sets --save-json
    
    # Custom directory with other options
    inkcollector --output-dir /project/data --profile complete lorcast get-sets

**Output Example:**

.. code-block:: text

    ============================================================
                        DISNEY LORCANA SETS                   
    ============================================================
    Found 5 sets:
    
    [JSON data displayed here if --json or profile.print_json is true]

lorcast get-cards
~~~~~~~~~~~~~~~~~

Retrieve detailed card information for a specific set.

**Syntax:**

.. code-block:: shell

    inkcollector lorcast get-cards --set-id SET_ID [OPTIONS]

**Required Arguments:**

.. option:: --set-id SET_ID

   The ID of the card set to retrieve cards from.
   
   **Examples:** ``TFC``, ``ROF``, ``ITI``

**Options:**

.. option:: --json

   Print JSON card data to console with formatted output.
   
   **Note:** Overrides profile's ``print_json`` setting.

.. option:: --save-json

   Save card data to configured data output directory.
   
   **Note:** Overrides profile's ``save_json`` setting.

.. option:: --get-images [SIZE]

   Download card images with specified size.
   
   **Choices:** ``small``, ``normal``, ``large``
   
   **Default:** ``normal`` (when flag is used without size)
   
   **Note:** Overrides profile's ``extract_images`` and ``image_size`` settings.

**Behavior:**

- Validates set ID by fetching set information first
- Retrieves all cards for the specified set
- Displays number of cards found
- Creates necessary directories automatically
- **Default mode:** Saves data to ``{data_output_dir}/lorcast/sets/{set_id}.json``
- **Custom data directory mode:** When ``--output-dir`` is used, saves data directly to ``{output_dir}/{set_id}.json`` (bypasses ``lorcast/sets/`` subdirectory)
- **Default mode:** Saves images to ``{image_output_dir}/lorcast/sets/{set_id}/``
- **Custom image directory mode:** When ``--image-dir`` is used, saves images directly to ``{image_dir}/`` (bypasses ``lorcast/sets/{set_id}/`` subdirectory)
- Images named as ``crd_{card_id}.jpg``
- Reports download success/failure statistics

**Examples:**

.. code-block:: shell

    # Get cards with profile defaults
    inkcollector lorcast get-cards --set-id TFC
    
    # Get cards and print to console
    inkcollector lorcast get-cards --set-id TFC --json
    
    # Get cards and save to file
    inkcollector lorcast get-cards --set-id TFC --save-json
    
    # Download normal-sized images
    inkcollector lorcast get-cards --set-id TFC --get-images
    
    # Download large-sized images
    inkcollector lorcast get-cards --set-id TFC --get-images large
    
    # Complete collection: data + images
    inkcollector lorcast get-cards --set-id TFC --json --save-json --get-images normal
    
    # With custom workspace
    inkcollector --workspace archive lorcast get-cards --set-id TFC --get-images
    
    # Custom data directory (full override)
    inkcollector --output-dir /project/cards lorcast get-cards --set-id TFC --save-json
    
    # Custom image directory (full override)
    inkcollector --image-dir /project/images lorcast get-cards --set-id TFC --get-images
    
    # Both custom directories
    inkcollector --output-dir /project/data --image-dir /project/images lorcast get-cards --set-id TFC --save-json --get-images
    
    # Mix custom directories with profiles
    inkcollector --output-dir /backup/data --profile complete lorcast get-cards --set-id TFC

**Output Example:**

.. code-block:: text

    ============================================================
                        DISNEY LORCANA CARDS                  
    ============================================================
    Found 204 cards in set TFC:
    
    [JSON data displayed here if --json or profile.print_json is true]
    
    Downloading images for 204 cards...
    Successfully downloaded 201 out of 204 card images.

lorcast get-all-sets
~~~~~~~~~~~~~~~~~~~~

Automatically fetch all available sets and their complete card data in a single operation. This is a bulk command that combines ``get-sets`` and ``get-cards`` functionality.

**Syntax:**

.. code-block:: shell

    inkcollector lorcast get-all-sets [OPTIONS]

**Options:**

.. option:: --json

   Print JSON data to console with formatted output for both sets and cards.
   
   **Note:** Overrides profile's ``print_json`` setting.

.. option:: --save-json

   Save JSON data to configured data output directory.
   
   **Note:** Overrides profile's ``save_json`` setting.

.. option:: --get-images [SIZE]

   Download card images for all sets with specified size.
   
   **Choices:** ``small``, ``normal``, ``large``
   
   **Default:** ``normal`` (when flag is used without size)
   
   **Note:** Overrides profile's ``extract_images`` and ``image_size`` settings.

**Behavior:**

- Fetches all available sets from the Lorcast API
- For each set, retrieves all card data automatically
- Displays progress information for each set processed
- Creates necessary directories automatically
- Continues processing remaining sets if individual set fails
- **Default mode:** 
  - Saves sets data to ``{data_output_dir}/lorcast/sets.json``
  - Saves each set's cards to ``{data_output_dir}/lorcast/sets/{set_id}.json``
  - Saves images to ``{image_output_dir}/lorcast/sets/{set_id}/``
- **Custom directory mode:** 
  - When ``--output-dir`` is used, saves data directly without ``lorcast/`` subdirectories
  - When ``--image-dir`` is used, saves images directly without ``lorcast/sets/{set_id}/`` subdirectories
- Images named as ``crd_{card_id}.jpg``
- Reports comprehensive download statistics at the end

**Examples:**

.. code-block:: shell

    # Use profile defaults (most common usage)
    inkcollector lorcast get-all-sets
    
    # Print all data to console
    inkcollector lorcast get-all-sets --json
    
    # Save all data to files
    inkcollector lorcast get-all-sets --save-json
    
    # Download all cards with normal-sized images
    inkcollector lorcast get-all-sets --get-images
    
    # Download all cards with large-sized images
    inkcollector lorcast get-all-sets --get-images large
    
    # Complete bulk collection: data + images
    inkcollector lorcast get-all-sets --json --save-json --get-images normal
    
    # With custom workspace for organization
    inkcollector --workspace complete-collection lorcast get-all-sets --get-images
    
    # Custom data directory (full override)
    inkcollector --output-dir /bulk/data lorcast get-all-sets --save-json
    
    # Custom image directory (full override)  
    inkcollector --image-dir /bulk/images lorcast get-all-sets --get-images
    
    # Both custom directories for bulk operation
    inkcollector --output-dir /project/data --image-dir /project/images lorcast get-all-sets --save-json --get-images
    
    # Use with specific profile for bulk operations
    inkcollector --profile complete lorcast get-all-sets

**Output Example:**

.. code-block:: text

    ============================================================
                    DISNEY LORCANA BULK COLLECTION            
    ============================================================
    Found 5 sets to process:
    
    Processing set 1/5: The First Chapter (TFC)...
    Found 204 cards in set TFC
    [Processing continues for each set...]
    
    Processing set 5/5: Shimmering Skies (SSK)...
    Found 204 cards in set SSK
    
    ============================================================
                        BULK OPERATION SUMMARY                
    ============================================================
    Successfully processed: 5/5 sets
    Total cards collected: 1,020 cards
    
    [Image download summary if --get-images used:]
    Image Download Summary:
    - Successfully downloaded: 1,015/1,020 images
    - Failed downloads: 5 images
    - Success rate: 99.5%

**Use Cases:**

This command is ideal for:

- Initial complete data collection
- Periodic full synchronization
- Research projects requiring complete datasets
- Backup and archival operations
- Setting up new development environments

**Performance Considerations:**

- This is a long-running operation that processes all available sets
- Consider disk space requirements before downloading images for all sets
- Use ``--profile preview`` first to see what sets will be processed
- Network timeouts may occur with large image downloads

Command Combinations
===================

Profile and Global Option Interactions
--------------------------------------

Global options override profile settings:

.. code-block:: shell

    # Profile says print_json=false, but --json overrides it
    inkcollector --profile data-only lorcast get-sets --json
    
    # Profile says extract_images=false, but --get-images overrides it
    inkcollector --profile data-only lorcast get-cards --set-id TFC --get-images

Custom Directory Override Behavior
----------------------------------

Custom directory flags provide complete path control:

.. code-block:: shell

    # Default behavior: uses lorcast/ subdirectories
    inkcollector lorcast get-sets --save-json
    # → Saves to: {workspace.data_output_dir}/lorcast/sets.json
    
    # Custom directory: full override, no subdirectories
    inkcollector --output-dir /my/data lorcast get-sets --save-json
    # → Saves to: /my/data/sets.json
    
    # Default behavior: uses lorcast/sets/{set-id}/ subdirectories
    inkcollector lorcast get-cards --set-id TFC --get-images
    # → Saves to: {workspace.image_output_dir}/lorcast/sets/TFC/
    
    # Custom directory: full override, no subdirectories
    inkcollector --image-dir /my/images lorcast get-cards --set-id TFC --get-images
    # → Saves to: /my/images/

Custom directories can be mixed with other options:

.. code-block:: shell

    # Custom data directory with workspace
    inkcollector --workspace research --output-dir /backup/data lorcast get-sets --save-json
    
    # Custom directories with profiles
    inkcollector --output-dir /project/data --image-dir /project/images --profile complete lorcast get-cards --set-id TFC

Multiple Workspaces
-------------------

.. code-block:: shell

    # Collect to different workspaces
    inkcollector --workspace research lorcast get-sets
    inkcollector --workspace archive lorcast get-cards --set-id TFC --get-images
    inkcollector --workspace website lorcast get-cards --set-id TFC --get-images small

Exit Codes
==========

Inkcollector uses standard exit codes:

.. list-table::
   :widths: 10 90
   :header-rows: 1

   * - Code
     - Meaning
   * - 0
     - Success
   * - 1
     - General error (network, API, file system)
   * - 2
     - Command line argument error
   * - 3
     - Configuration error

Error Handling
==============

Inkcollector provides detailed error messages for common issues:

Network Errors
--------------

.. code-block:: text

    Error: Failed to connect to Lorcast API
    - Check your internet connection
    - Verify the API is accessible: https://api.lorcast.com

Invalid Set ID
--------------

.. code-block:: text

    Error: Set ID 'INVALID' not found
    - Use 'inkcollector --profile preview lorcast get-sets' to see available sets
    - Check spelling and case sensitivity

Permission Errors
-----------------

.. code-block:: text

    Error: Permission denied creating directory 'data/lorcast'
    - Check write permissions for the target directory
    - Try running with appropriate privileges

File System Errors
------------------

.. code-block:: text

    Error: Disk full while saving images
    - Free up disk space
    - Use a different output directory with --workspace

Configuration Errors
--------------------

.. code-block:: text

    Error: Profile 'myprofile' not found in configuration
    - Check available profiles: inkcollector config list --profiles
    - Verify profile name spelling

Tips and Best Practices
=======================

Performance Tips
---------------

- Use ``--profile preview`` to explore data before downloading
- Download images in smaller sizes for faster transfers
- Use ``--profile data-only`` when you only need metadata
- Batch similar operations to the same workspace

Workflow Tips
------------

- Check available sets first: ``inkcollector --profile preview lorcast get-sets``
- Verify set IDs before bulk operations
- Use meaningful workspace names for organization
- Create custom profiles for repeated operations

Safety Tips
----------

- Always verify disk space before large image downloads
- Use test workspaces for experiments
- Keep configuration files in version control
- Backup important data before major operations

See Also
========

- :doc:`configuration` - Configuration file system
- :doc:`profiles-workspaces` - Profile and workspace details
- :doc:`examples` - Real-world usage examples
- :doc:`troubleshooting` - Common issues and solutions
