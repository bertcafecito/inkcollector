.. _installation:

============
Installation
============

This guide walks you through installing Inkcollector on your system.

Prerequisites
=============

Inkcollector requires **Python 3.9 or later**. Check your Python version:

.. code-block:: shell

    python --version

If you need to install or update Python, visit `python.org <https://www.python.org/downloads/>`_.

Installing from PyPI
====================

The easiest way to install Inkcollector is from PyPI using pip:

.. code-block:: shell

    pip install inkcollector

This installs the latest stable version of Inkcollector and all required dependencies.

Virtual Environment (Recommended)
=================================

We strongly recommend installing Inkcollector in a virtual environment to avoid conflicts with system packages:

Using venv (Built-in)
----------------------

.. code-block:: shell

    # Create a virtual environment
    python -m venv inkcollector-env
    
    # Activate it (Windows)
    inkcollector-env\Scripts\activate
    
    # Activate it (macOS/Linux)
    source inkcollector-env/bin/activate
    
    # Install Inkcollector
    pip install inkcollector

Using conda
-----------

.. code-block:: shell

    # Create a conda environment
    conda create -n inkcollector python=3.11
    
    # Activate it
    conda activate inkcollector
    
    # Install Inkcollector
    pip install inkcollector

Development Installation
=======================

If you want to contribute to Inkcollector or use the latest development version:

.. code-block:: shell

    # Clone the repository
    git clone https://github.com/bertcafecito/inkcollector.git
    cd inkcollector
    
    # Create virtual environment
    python -m venv venv
    source venv/bin/activate  # or venv\Scripts\activate on Windows
    
    # Install in development mode
    pip install -e .
    
    # Install development dependencies
    pip install -e ".[dev,docs]"

Verifying Installation
=====================

After installation, verify that Inkcollector is working correctly:

.. code-block:: shell

    # Check version
    inkcollector --version
    
    # View help
    inkcollector --help
    
    # Test basic functionality
    inkcollector config init

If the commands work without errors, Inkcollector is successfully installed!

Updating Inkcollector
====================

To update to the latest version:

.. code-block:: shell

    pip install --upgrade inkcollector

Uninstalling
============

To remove Inkcollector:

.. code-block:: shell

    pip uninstall inkcollector

Troubleshooting Installation
===========================

Permission Errors
-----------------

If you encounter permission errors on Windows or macOS:

.. code-block:: shell

    # Use --user flag
    pip install --user inkcollector

Network Issues
--------------

If you're behind a corporate firewall or proxy:

.. code-block:: shell

    # Use proxy
    pip install --proxy http://user:password@proxy.server:port inkcollector
    
    # Or use trusted hosts
    pip install --trusted-host pypi.org --trusted-host pypi.python.org inkcollector

Python Version Issues
---------------------

If you have multiple Python versions installed, make sure you're using the right one:

.. code-block:: shell

    # Use specific Python version
    python3.11 -m pip install inkcollector
    
    # Or use full path
    /usr/bin/python3 -m pip install inkcollector

Dependencies
============

Inkcollector automatically installs these required dependencies:

- **requests** (>=2.32.3): HTTP library for API communication
- **PyYAML** (>=6.0): YAML parser for configuration files

Optional Dependencies
====================

For documentation building:

.. code-block:: shell

    pip install "inkcollector[docs]"

For development:

.. code-block:: shell

    pip install "inkcollector[dev]"

For everything:

.. code-block:: shell

    pip install "inkcollector[dev,docs]"

Next Steps
==========

Once installed, head over to the :doc:`quickstart` guide to begin using Inkcollector!
