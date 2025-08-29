.. _quickstart:

==========
Quickstart
==========

This guide gets you up and running with Inkcollector in just a few minutes.

First Run
=========

After :doc:`installation`, let's verify everything works:

.. code-block:: shell

    # Check version
    inkcollector --version
    
    # View available commands
    inkcollector --help

Setting Up Configuration
========================

Inkcollector works great out of the box, but configuration files make it much more powerful:

.. code-block:: shell

    # Create a configuration file with defaults
    inkcollector config init
    
    # View your configuration
    inkcollector config show

This creates a ``.inkcollector.yaml`` file in your current directory with sensible defaults.

Your First Data Collection
==========================

Let's collect some Disney Lorcana data! 

Fetch All Card Sets
-------------------

.. code-block:: shell

    # Get all available sets (saves to data/ directory)
    inkcollector lorcast get-sets

This command:

- Fetches all Disney Lorcana card sets from the Lorcast API
- Saves the data to ``data/lorcast/sets.json``
- Shows you how many sets were found

Get Cards from a Specific Set
-----------------------------

.. code-block:: shell

    # Get cards from "The First Chapter" set
    inkcollector lorcast get-cards --set-id TFC

This command:

- Fetches all cards from the TFC (The First Chapter) set
- Saves card data to ``data/lorcast/sets/TFC.json``
- Shows you how many cards were found

Download Card Images
-------------------

.. code-block:: shell

    # Get cards AND download images
    inkcollector lorcast get-cards --set-id TFC --get-images

This downloads:

- Card data to ``data/lorcast/sets/TFC.json``
- Card images to ``images/lorcast/sets/TFC/``
- Images are named like ``crd_001.jpg``, ``crd_002.jpg``, etc.

Understanding Profiles
======================

Inkcollector comes with built-in profiles for different use cases:

Preview Profile (Console Only)
------------------------------

.. code-block:: shell

    # Just show data in console, don't save files
    inkcollector --profile preview lorcast get-sets

Images Only Profile
------------------

.. code-block:: shell

    # Only download images, skip data files
    inkcollector --profile images-only lorcast get-cards --set-id TFC

Data Only Profile
----------------

.. code-block:: shell

    # Only save data files, skip images
    inkcollector --profile data-only lorcast get-cards --set-id TFC

Complete Profile (Default)
--------------------------

.. code-block:: shell

    # Save data files AND download images (this is the default)
    inkcollector --profile complete lorcast get-cards --set-id TFC --get-images

Exploring Your Data
===================

After running the commands above, your directory structure looks like:

.. code-block:: text

    your-project/
    ├── .inkcollector.yaml          # Your configuration
    ├── data/
    │   └── lorcast/
    │       ├── sets.json           # All sets data
    │       └── sets/
    │           └── TFC.json        # TFC set card data
    └── images/
        └── lorcast/
            └── sets/
                └── TFC/
                    ├── crd_001.jpg # Card images
                    ├── crd_002.jpg
                    └── ...

Quick Examples
==============

Common Workflows
---------------

**Research Workflow** (data only):

.. code-block:: shell

    inkcollector --profile data-only lorcast get-sets
    inkcollector --profile data-only lorcast get-cards --set-id TFC
    inkcollector --profile data-only lorcast get-cards --set-id ROF

**Collection Catalog** (images only):

.. code-block:: shell

    inkcollector --profile images-only lorcast get-cards --set-id TFC --get-images
    inkcollector --profile images-only lorcast get-cards --set-id ROF --get-images

**Complete Archive** (everything):

.. code-block:: shell

    inkcollector lorcast get-sets
    inkcollector lorcast get-cards --set-id TFC --get-images
    inkcollector lorcast get-cards --set-id ROF --get-images

Finding Set IDs
---------------

To find available set IDs:

.. code-block:: shell

    # View sets in console
    inkcollector --profile preview lorcast get-sets

Look for the ``id`` field in each set (like ``TFC``, ``ROF``, etc.).

Next Steps
==========

Now that you're familiar with the basics:

1. **Learn about configuration**: Read the :doc:`configuration` guide to customize profiles and workspaces
2. **Explore all commands**: Check the :doc:`cli-reference` for detailed command documentation  
3. **See more examples**: Browse the :doc:`examples` section for advanced usage patterns
4. **Customize your setup**: Create custom profiles and workspaces in your configuration file

Tips for New Users
==================

💡 **Pro Tips:**

- Use ``--profile preview`` to explore data before saving files
- The ``config show`` command helps you understand your current settings
- Set IDs are usually short codes like ``TFC``, ``ROF``, ``ITI``
- Images can be quite large - use ``--get-images small`` for thumbnails
- Check ``config list`` to see all available profiles and workspaces

🚨 **Common Gotchas:**

- Make sure you have an internet connection for API calls
- Some sets might have many cards - image downloads can take time
- Configuration files are searched in current directory and up to 3 parent directories
- Profile and workspace names are case-sensitive

Need Help?
==========

If you run into issues:

- Check the :doc:`troubleshooting` section
- Use ``inkcollector --help`` or ``inkcollector lorcast --help`` for command help
- Look at the :doc:`examples` for more usage patterns
- Report bugs on `GitHub <https://github.com/bertcafecito/inkcollector/issues>`_
