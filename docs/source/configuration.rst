.. _configuration:

=============
Configuration
=============

Inkcollector's YAML configuration system provides powerful customization options through profiles and workspaces.

Overview
========

Configuration files allow you to:

- Define **extraction profiles** for different use cases
- Set up **workspaces** for different environments or projects  
- Customize **default settings** and **API endpoints**
- Create **reusable workflows** for data collection

Configuration files are named ``.inkcollector.yaml`` and are automatically discovered in your current directory or up to 3 parent directories.

Getting Started
===============

Creating Your First Config
---------------------------

.. code-block:: shell

    # Create default configuration
    inkcollector config init
    
    # Create config at specific path
    inkcollector config init --path my-config.yaml

Viewing Configuration
--------------------

.. code-block:: shell

    # Show current configuration (YAML format)
    inkcollector config show
    
    # Show in JSON format
    inkcollector config show --format json
    
    # List available profiles and workspaces
    inkcollector config list

Configuration Structure
=======================

A complete configuration file has four main sections:

.. code-block:: yaml

    # Default workspace when none is specified
    default_workspace: default

    # API configuration
    api_base_url: https://api.lorcast.com
    api_version: v0

    # Extraction profiles define what data to collect
    profiles:
      my-profile:
        description: "Custom profile description"
        extract_data: true      # Extract JSON data
        extract_images: true    # Download images  
        image_size: normal      # Image size: small, normal, large
        save_json: true         # Save JSON to files
        print_json: false       # Print JSON to console

    # Workspaces define output directories and defaults
    workspaces:
      my-workspace:
        data_output_dir: data           # Where to save JSON files
        image_output_dir: images        # Where to save images
        default_profile: my-profile     # Default profile for this workspace

Extraction Profiles
===================

Profiles define **what** data to extract and **how** to handle it.

Built-in Profiles
-----------------

Inkcollector comes with four pre-configured profiles:

**complete** (Default)
^^^^^^^^^^^^^^^^^^^^^^

Extract everything and save to files:

.. code-block:: yaml

    complete:
      description: "Extract all data and images"
      extract_data: true
      extract_images: true
      image_size: normal
      save_json: true
      print_json: false

Usage: ``inkcollector --profile complete lorcast get-cards --set-id TFC --get-images``

**images-only**
^^^^^^^^^^^^^^^

Only download card images:

.. code-block:: yaml

    images-only:
      description: "Extract only card images"
      extract_data: false
      extract_images: true
      image_size: normal
      save_json: false
      print_json: false

Usage: ``inkcollector --profile images-only lorcast get-cards --set-id TFC --get-images``

**data-only**
^^^^^^^^^^^^^

Only extract and save JSON data:

.. code-block:: yaml

    data-only:
      description: "Extract only JSON data"
      extract_data: true
      extract_images: false
      image_size: normal
      save_json: true
      print_json: false

Usage: ``inkcollector --profile data-only lorcast get-cards --set-id TFC``

**preview**
^^^^^^^^^^^

Show data in console without saving files:

.. code-block:: yaml

    preview:
      description: "Show data in console without saving"
      extract_data: true
      extract_images: false
      image_size: normal
      save_json: false
      print_json: true

Usage: ``inkcollector --profile preview lorcast get-sets``

Custom Profiles
---------------

Create profiles for specific workflows:

**Research Profile** (High-quality images, data saved):

.. code-block:: yaml

    profiles:
      research:
        description: "High-quality images and data for research"
        extract_data: true
        extract_images: true
        image_size: large
        save_json: true
        print_json: false

**Thumbnail Profile** (Small images for quick previews):

.. code-block:: yaml

    profiles:
      thumbnails:
        description: "Small images for quick previews"
        extract_data: false
        extract_images: true
        image_size: small
        save_json: false
        print_json: false

**Analysis Profile** (Data only with console output):

.. code-block:: yaml

    profiles:
      analysis:
        description: "Data analysis with console output"
        extract_data: true
        extract_images: false
        image_size: normal
        save_json: true
        print_json: true

Workspaces
==========

Workspaces define **where** data is saved and **default behaviors** for different environments.

Default Workspace
-----------------

The built-in default workspace:

.. code-block:: yaml

    workspaces:
      default:
        data_output_dir: data
        image_output_dir: images
        default_profile: complete

This creates the structure:

.. code-block:: text

    your-project/
    ├── data/
    │   └── lorcast/
    └── images/
        └── lorcast/

Custom Workspaces
-----------------

**Project Workspace** (Organized by project):

.. code-block:: yaml

    workspaces:
      project-alpha:
        data_output_dir: projects/alpha/data
        image_output_dir: projects/alpha/images
        default_profile: research

**Archive Workspace** (Long-term storage):

.. code-block:: yaml

    workspaces:
      archive:
        data_output_dir: archive/lorcana-data
        image_output_dir: archive/lorcana-images
        default_profile: complete

**Development Workspace** (Testing and development):

.. code-block:: yaml

    workspaces:
      dev:
        data_output_dir: tmp/dev-data
        image_output_dir: tmp/dev-images
        default_profile: preview

Usage Examples
==============

Using Custom Configurations
---------------------------

.. code-block:: shell

    # Use specific workspace
    inkcollector --workspace project-alpha lorcast get-sets
    
    # Override profile in workspace
    inkcollector --workspace archive --profile thumbnails lorcast get-cards --set-id TFC
    
    # Use custom config file
    inkcollector --config my-config.yaml lorcast get-sets

Complete Example Configuration
-----------------------------

Here's a comprehensive configuration for different scenarios:

.. code-block:: yaml

    # Default workspace for most operations
    default_workspace: main

    # API settings (usually don't need to change)
    api_base_url: https://api.lorcast.com
    api_version: v0

    # Custom profiles for different use cases
    profiles:
      # Quick data exploration
      explore:
        description: "Quick data exploration in console"
        extract_data: true
        extract_images: false
        save_json: false
        print_json: true

      # Complete archival
      archive:
        description: "Complete archival with high-quality images"
        extract_data: true
        extract_images: true
        image_size: large
        save_json: true
        print_json: false

      # Website thumbnails
      web-thumbs:
        description: "Small images for website use"
        extract_data: false
        extract_images: true
        image_size: small
        save_json: false
        print_json: false

      # Research data
      research:
        description: "Research data with normal images"
        extract_data: true
        extract_images: true
        image_size: normal
        save_json: true
        print_json: true

    # Workspaces for different projects
    workspaces:
      # Main workspace for daily use
      main:
        data_output_dir: data
        image_output_dir: images
        default_profile: complete

      # Research project
      research-proj:
        data_output_dir: research/lorcana-data
        image_output_dir: research/lorcana-images
        default_profile: research

      # Website assets
      website:
        data_output_dir: website/data
        image_output_dir: website/assets/images
        default_profile: web-thumbs

      # Long-term archive
      backup:
        data_output_dir: backups/lorcana/data
        image_output_dir: backups/lorcana/images
        default_profile: archive

Configuration Priority
======================

Settings are applied in this order (later overrides earlier):

1. **Built-in defaults**
2. **Configuration file settings**
3. **Command-line global options** (``--workspace``, ``--profile``)
4. **Command-line flags** (``--json``, ``--save-json``, ``--get-images``)

Example:

.. code-block:: shell

    # This command uses:
    # 1. 'research-proj' workspace (from --workspace)
    # 2. 'web-thumbs' profile (from --profile)  
    # 3. JSON printing enabled (from --json flag)
    inkcollector --workspace research-proj --profile web-thumbs --json lorcast get-sets

Advanced Configuration
=====================

Environment-Specific Configs
----------------------------

You can have different configs for different environments:

.. code-block:: shell

    # Development
    inkcollector --config .inkcollector.dev.yaml lorcast get-sets
    
    # Production
    inkcollector --config .inkcollector.prod.yaml lorcast get-sets

Configuration Validation
------------------------

Inkcollector validates your configuration and will show helpful error messages:

.. code-block:: shell

    # Check if your config is valid
    inkcollector config show

Best Practices
==============

📋 **Organization Tips:**

- Use descriptive profile and workspace names
- Group related profiles (e.g., ``web-small``, ``web-large``)
- Create workspaces for different projects or environments
- Document profile purposes in the ``description`` field

🎯 **Workflow Tips:**

- Start with built-in profiles, then customize as needed
- Use ``preview`` profile to explore data before saving
- Create a ``testing`` workspace for experiments
- Use meaningful directory names in workspaces

🔧 **Maintenance Tips:**

- Use ``config show`` to verify settings
- Use ``config list`` to see available options
- Keep configuration files in version control
- Comment your custom configurations

Troubleshooting
===============

Config Not Found
----------------

.. code-block:: text

    Error: Configuration file not found

**Solution:** Make sure ``.inkcollector.yaml`` exists in current directory or parent directories, or specify path with ``--config``.

Invalid Profile/Workspace
-------------------------

.. code-block:: text

    Error: Profile 'myprofile' not found

**Solution:** Check available profiles with ``inkcollector config list --profiles``.

Permission Errors
-----------------

.. code-block:: text

    Error: Cannot create directory

**Solution:** Check that you have write permissions to the configured output directories.

Next Steps
==========

- Learn about all CLI commands in :doc:`cli-reference`
- See real-world examples in :doc:`examples`
- Explore workspace and profile combinations in :doc:`profiles-workspaces`
