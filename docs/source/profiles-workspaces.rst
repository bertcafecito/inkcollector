.. _profiles-workspaces:

====================
Profiles & Workspaces
====================

Deep dive into Inkcollector's profile and workspace system for maximum flexibility and organization.

Understanding the System
========================

Inkcollector's configuration system has two main concepts:

**Profiles** define **WHAT** to do:
   - What data to extract (JSON, images, or both)
   - How to handle the data (save to files, print to console)
   - What image size to download

**Workspaces** define **WHERE** to put things:
   - Output directory structure
   - Default profile to use
   - Environment-specific settings

Together, they create powerful and flexible workflows.

Built-in Profiles
=================

complete
--------

**Purpose:** Default profile for comprehensive data collection.

.. code-block:: yaml

    complete:
      description: "Extract all data and images"
      extract_data: true      # ✓ Get JSON data
      extract_images: true    # ✓ Download images when --get-images used
      image_size: normal      # Normal resolution images
      save_json: true         # ✓ Save data to files
      print_json: false       # Don't clutter console

**Best for:**
- General data collection
- Building complete archives
- Default everyday usage

**Example usage:**

.. code-block:: shell

    # Uses complete profile (default)
    inkcollector lorcast get-sets
    inkcollector lorcast get-cards --set-id TFC --get-images

images-only
-----------

**Purpose:** Focus only on downloading card images.

.. code-block:: yaml

    images-only:
      description: "Extract only card images"
      extract_data: false     # Skip JSON data
      extract_images: true    # ✓ Download images when --get-images used
      image_size: normal      # Normal resolution images
      save_json: false        # Don't save JSON files
      print_json: false       # Don't print to console

**Best for:**
- Building image galleries
- Website asset collection
- Visual-only projects

**Example usage:**

.. code-block:: shell

    inkcollector --profile images-only lorcast get-cards --set-id TFC --get-images
    inkcollector --profile images-only lorcast get-cards --set-id ROF --get-images large

data-only
---------

**Purpose:** Extract only JSON data without images.

.. code-block:: yaml

    data-only:
      description: "Extract only JSON data"
      extract_data: true      # ✓ Get JSON data
      extract_images: false   # Skip images
      image_size: normal      # (ignored since extract_images=false)
      save_json: true         # ✓ Save data to files
      print_json: false       # Don't clutter console

**Best for:**
- Data analysis projects
- Metadata collection
- API research and development

**Example usage:**

.. code-block:: shell

    inkcollector --profile data-only lorcast get-sets
    inkcollector --profile data-only lorcast get-cards --set-id TFC

preview
-------

**Purpose:** Explore data in console without saving files.

.. code-block:: yaml

    preview:
      description: "Show data in console without saving"
      extract_data: true      # ✓ Get JSON data
      extract_images: false   # Skip images
      image_size: normal      # (ignored)
      save_json: false        # Don't create files
      print_json: true        # ✓ Show in console

**Best for:**
- Exploring available data
- Quick data inspection
- Learning about the API structure

**Example usage:**

.. code-block:: shell

    # See what sets are available
    inkcollector --profile preview lorcast get-sets
    
    # Preview cards in a set
    inkcollector --profile preview lorcast get-cards --set-id TFC

Custom Profile Examples
=======================

Research Profile
----------------

High-quality images and comprehensive data for research projects:

.. code-block:: yaml

    profiles:
      research:
        description: "High-quality data and images for research"
        extract_data: true
        extract_images: true
        image_size: large       # High resolution
        save_json: true
        print_json: true        # Also show in console for verification

**Usage:**

.. code-block:: shell

    inkcollector --profile research lorcast get-cards --set-id TFC --get-images

Web Assets Profile
------------------

Small images optimized for web use:

.. code-block:: yaml

    profiles:
      web-assets:
        description: "Small images for web use"
        extract_data: false
        extract_images: true
        image_size: small       # Small thumbnails
        save_json: false
        print_json: false

**Usage:**

.. code-block:: shell

    inkcollector --profile web-assets lorcast get-cards --set-id TFC --get-images

Debug Profile
-------------

Detailed console output for debugging:

.. code-block:: yaml

    profiles:
      debug:
        description: "Detailed output for debugging"
        extract_data: true
        extract_images: false
        image_size: normal
        save_json: true
        print_json: true        # Show everything in console

**Usage:**

.. code-block:: shell

    inkcollector --profile debug lorcast get-cards --set-id TFC

Archive Profile
---------------

Complete archival with high-quality images:

.. code-block:: yaml

    profiles:
      archive:
        description: "Complete archival with large images"
        extract_data: true
        extract_images: true
        image_size: large
        save_json: true
        print_json: false

**Usage:**

.. code-block:: shell

    inkcollector --profile archive lorcast get-cards --set-id TFC --get-images

Default Workspace
=================

The built-in default workspace provides a standard directory structure:

.. code-block:: yaml

    workspaces:
      default:
        data_output_dir: data
        image_output_dir: images
        default_profile: complete

**Creates this structure:**

.. code-block:: text

    your-project/
    ├── data/
    │   └── lorcast/
    │       ├── sets.json
    │       └── sets/
    │           ├── TFC.json
    │           └── ROF.json
    └── images/
        └── lorcast/
            └── sets/
                ├── TFC/
                │   ├── crd_001.jpg
                │   └── crd_002.jpg
                └── ROF/
                    ├── crd_001.jpg
                    └── crd_002.jpg

Custom Workspace Examples
=========================

Project-Based Workspace
-----------------------

Organize by specific projects:

.. code-block:: yaml

    workspaces:
      lorcana-analytics:
        data_output_dir: projects/lorcana-analytics/data
        image_output_dir: projects/lorcana-analytics/images
        default_profile: research

**Creates:**

.. code-block:: text

    projects/
    └── lorcana-analytics/
        ├── data/
        │   └── lorcast/
        └── images/
            └── lorcast/

**Usage:**

.. code-block:: shell

    inkcollector --workspace lorcana-analytics lorcast get-sets

Environment Workspaces
----------------------

Separate development, staging, and production:

.. code-block:: yaml

    workspaces:
      development:
        data_output_dir: dev/data
        image_output_dir: dev/images
        default_profile: preview

      staging:
        data_output_dir: staging/data
        image_output_dir: staging/images
        default_profile: data-only

      production:
        data_output_dir: prod/data
        image_output_dir: prod/images
        default_profile: complete

**Usage:**

.. code-block:: shell

    # Development (preview only)
    inkcollector --workspace development lorcast get-sets
    
    # Staging (data only)
    inkcollector --workspace staging lorcast get-cards --set-id TFC
    
    # Production (complete data)
    inkcollector --workspace production lorcast get-cards --set-id TFC --get-images

Archive Workspace
-----------------

Long-term storage with organized structure:

.. code-block:: yaml

    workspaces:
      archive:
        data_output_dir: archives/lorcana/data
        image_output_dir: archives/lorcana/images
        default_profile: archive

**Creates:**

.. code-block:: text

    archives/
    └── lorcana/
        ├── data/
        │   └── lorcast/
        └── images/
            └── lorcast/

Website Workspace
-----------------

Assets organized for website deployment:

.. code-block:: yaml

    workspaces:
      website:
        data_output_dir: website/api/data
        image_output_dir: website/public/images/cards
        default_profile: web-assets

**Creates:**

.. code-block:: text

    website/
    ├── api/
    │   └── data/
    │       └── lorcast/
    └── public/
        └── images/
            └── cards/
                └── lorcast/

Advanced Combinations
====================

Profile + Workspace Combinations
--------------------------------

Different profiles work better with different workspaces:

.. code-block:: shell

    # Research workflow
    inkcollector --workspace lorcana-analytics --profile research lorcast get-cards --set-id TFC --get-images
    
    # Website asset generation
    inkcollector --workspace website --profile web-assets lorcast get-cards --set-id TFC --get-images
    
    # Development testing
    inkcollector --workspace development --profile preview lorcast get-sets
    
    # Production archival
    inkcollector --workspace archive --profile archive lorcast get-cards --set-id TFC --get-images

Override Patterns
-----------------

Global options override workspace defaults:

.. code-block:: shell

    # Use archive workspace but override with preview profile
    inkcollector --workspace archive --profile preview lorcast get-sets
    
    # Use web workspace but force large images
    inkcollector --workspace website lorcast get-cards --set-id TFC --get-images large

Configuration Management
========================

Multi-Environment Setup
-----------------------

Use different config files for different environments:

**`.inkcollector.dev.yaml`** (Development):

.. code-block:: yaml

    default_workspace: development
    profiles:
      dev-test:
        description: "Quick testing"
        extract_data: true
        extract_images: false
        save_json: false
        print_json: true
    workspaces:
      development:
        data_output_dir: tmp/dev-data
        image_output_dir: tmp/dev-images
        default_profile: dev-test

**`.inkcollector.prod.yaml`** (Production):

.. code-block:: yaml

    default_workspace: production
    profiles:
      prod-complete:
        description: "Production-ready complete extraction"
        extract_data: true
        extract_images: true
        image_size: large
        save_json: true
        print_json: false
    workspaces:
      production:
        data_output_dir: data/lorcana
        image_output_dir: assets/images/lorcana
        default_profile: prod-complete

**Usage:**

.. code-block:: shell

    # Development
    inkcollector --config .inkcollector.dev.yaml lorcast get-sets
    
    # Production
    inkcollector --config .inkcollector.prod.yaml lorcast get-cards --set-id TFC --get-images

Team Configuration
-----------------

Share configurations across team members:

**`team-config.yaml`**:

.. code-block:: yaml

    default_workspace: shared

    profiles:
      team-research:
        description: "Standard research profile for team"
        extract_data: true
        extract_images: true
        image_size: normal
        save_json: true
        print_json: false

      team-assets:
        description: "Standard asset profile for team"
        extract_data: false
        extract_images: true
        image_size: small
        save_json: false
        print_json: false

    workspaces:
      shared:
        data_output_dir: shared/data
        image_output_dir: shared/images
        default_profile: team-research

      personal:
        data_output_dir: personal/data
        image_output_dir: personal/images
        default_profile: team-research

**Usage:**

.. code-block:: shell

    # Team member using shared config
    inkcollector --config team-config.yaml --workspace shared lorcast get-sets
    
    # Personal workspace with team profiles
    inkcollector --config team-config.yaml --workspace personal --profile team-assets lorcast get-cards --set-id TFC --get-images

Best Practices
==============

Profile Design
--------------

📋 **Profile Guidelines:**

- Use descriptive names (``web-thumbnails`` vs ``profile1``)
- Include meaningful descriptions
- Group related profiles (``research-data``, ``research-images``)
- Consider the end use case when setting options

🎯 **Common Patterns:**

- **Exploration profiles:** ``print_json=true``, ``save_json=false``
- **Production profiles:** ``print_json=false``, ``save_json=true``
- **Image-focused profiles:** ``extract_data=false``, ``extract_images=true``
- **Data-focused profiles:** ``extract_data=true``, ``extract_images=false``

Workspace Organization
---------------------

📁 **Directory Structure:**

- Use clear, hierarchical paths
- Consider deployment needs
- Plan for growth and scaling
- Keep related data together

🏗️ **Naming Conventions:**

- Environment-based: ``dev``, ``staging``, ``prod``
- Project-based: ``project-alpha``, ``project-beta``
- Purpose-based: ``research``, ``website``, ``archive``
- Team-based: ``shared``, ``personal``, ``client-work``

Configuration Maintenance
-------------------------

🔧 **Maintenance Tips:**

- Document custom profiles and workspaces
- Use version control for configuration files
- Test configurations before sharing with team
- Review and clean up unused profiles periodically

📊 **Monitoring:**

- Use ``config show`` to verify current settings
- Use ``config list`` to see all available options
- Check output directories periodically for disk usage
- Monitor image download sizes for cost/bandwidth

Next Steps
==========

- See real-world examples in :doc:`examples`
- Learn about troubleshooting in :doc:`troubleshooting`
- Check the complete command reference in :doc:`cli-reference`
