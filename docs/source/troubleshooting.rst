.. _troubleshooting:

===============
Troubleshooting
===============

Solutions to common issues and problems you might encounter while using Inkcollector.

Installation Issues
===================

Permission Errors
-----------------

**Problem:**

.. code-block:: text

    ERROR: Could not install packages due to an EnvironmentError: 
    [Errno 13] Permission denied

**Solutions:**

1. **Use virtual environment (recommended):**

   .. code-block:: shell

       python -m venv inkcollector-env
       # Windows
       inkcollector-env\Scripts\activate
       # macOS/Linux
       source inkcollector-env/bin/activate
       pip install inkcollector

2. **Install for current user only:**

   .. code-block:: shell

       pip install --user inkcollector

3. **Use elevated privileges (not recommended):**

   .. code-block:: shell

       # Windows (as Administrator)
       pip install inkcollector
       
       # macOS/Linux
       sudo pip install inkcollector

Python Version Issues
--------------------

**Problem:**

.. code-block:: text

    ERROR: Package 'inkcollector' requires a different Python: 
    3.8.0 not in '>=3.9'

**Solution:**

Inkcollector requires Python 3.9 or later. Check your Python version:

.. code-block:: shell

    python --version

**Options:**

1. **Update Python:** Download from `python.org <https://www.python.org/downloads/>`_

2. **Use a different Python version:**

   .. code-block:: shell

       # If you have multiple Python versions
       python3.9 -m pip install inkcollector
       python3.11 -m pip install inkcollector

3. **Use conda:**

   .. code-block:: shell

       conda create -n inkcollector python=3.11
       conda activate inkcollector
       pip install inkcollector

Network/Proxy Issues
--------------------

**Problem:**

.. code-block:: text

    ERROR: Could not fetch URL https://pypi.org/simple/inkcollector/

**Solutions:**

1. **Configure proxy:**

   .. code-block:: shell

       pip install --proxy http://user:password@proxy.server:port inkcollector

2. **Use trusted hosts:**

   .. code-block:: shell

       pip install --trusted-host pypi.org --trusted-host pypi.python.org inkcollector

3. **Check firewall settings:** Ensure Python/pip can access the internet

Configuration Issues
====================

Configuration File Not Found
----------------------------

**Problem:**

.. code-block:: text

    Warning: No configuration file found. Using default settings.

**Solution:**

Create a configuration file:

.. code-block:: shell

    # Create in current directory
    inkcollector config init
    
    # Or specify custom path
    inkcollector config init --path my-config.yaml
    
    # Or use existing config file
    inkcollector --config path/to/config.yaml lorcast get-sets

Invalid Configuration
--------------------

**Problem:**

.. code-block:: text

    Error: Profile 'myprofile' not found in configuration

**Solutions:**

1. **Check available profiles:**

   .. code-block:: shell

       inkcollector config list --profiles

2. **Verify spelling:**

   Profile names are case-sensitive. Check your configuration file.

3. **Show current configuration:**

   .. code-block:: shell

       inkcollector config show

4. **Fix common mistakes:**

   .. code-block:: yaml

       # Correct
       profiles:
         my-profile:  # Note: hyphens, not underscores
           description: "My custom profile"
       
       # Incorrect
       profiles:
         my_profile:  # Underscores might cause issues

YAML Syntax Errors
------------------

**Problem:**

.. code-block:: text

    Error: Invalid YAML syntax in configuration file

**Solutions:**

1. **Check indentation:** YAML uses spaces, not tabs

   .. code-block:: yaml

       # Correct (2 spaces)
       profiles:
         my-profile:
           description: "Profile description"
       
       # Incorrect (tabs or inconsistent spacing)
       profiles:
       	my-profile:
           description: "Profile description"

2. **Validate YAML syntax:** Use online YAML validators

3. **Check quotes:** Use quotes around strings with special characters

   .. code-block:: yaml

       # Use quotes for paths with spaces
       data_output_dir: "C:/Program Files/My App/data"

API and Network Issues
=====================

Connection Errors
-----------------

**Problem:**

.. code-block:: text

    Error: Failed to connect to Lorcast API
    ConnectionError: HTTPSConnectionPool(host='api.lorcast.com', port=443)

**Solutions:**

1. **Check internet connection:**

   .. code-block:: shell

       # Test basic connectivity
       ping api.lorcast.com
       
       # Test HTTPS access
       curl https://api.lorcast.com/v0/sets

2. **Check firewall/proxy settings:**

   - Ensure HTTPS traffic is allowed
   - Configure proxy if needed
   - Check corporate network restrictions

3. **Try different network:**

   - Switch to mobile hotspot
   - Try from different location
   - Test at different time of day

4. **Verify API status:**

   Check if the Lorcast API is operational

API Timeout Errors
-----------------

**Problem:**

.. code-block:: text

    Error: Request timed out after 30 seconds

**Solutions:**

1. **Retry the operation:**

   Temporary network issues may resolve

2. **Use preview profile first:**

   .. code-block:: shell

       # Test with smaller request
       inkcollector --profile preview lorcast get-sets

3. **Break into smaller chunks:**

   .. code-block:: shell

       # Get data first, images later
       inkcollector --profile data-only lorcast get-cards --set-id TFC
       inkcollector --profile images-only lorcast get-cards --set-id TFC --get-images

Invalid Set ID
-------------

**Problem:**

.. code-block:: text

    Error: Set ID 'INVALID' not found

**Solutions:**

1. **Check available sets:**

   .. code-block:: shell

       inkcollector --profile preview lorcast get-sets

2. **Verify set ID format:**

   - Set IDs are usually 3-letter codes: ``TFC``, ``ROF``, ``ITI``
   - They are case-sensitive
   - Use exact spelling from the sets list

3. **Common set IDs:**

   - ``TFC`` - The First Chapter
   - ``ROF`` - Rise of the Floodborn  
   - ``ITI`` - Into the Inklands
   - ``URR`` - Ursula's Return
   - ``SSK`` - Shimmering Skies

File System Issues
=================

Permission Denied
----------------

**Problem:**

.. code-block:: text

    Error: Permission denied creating directory 'data/lorcast'

**Solutions:**

1. **Use different output directory:**

   .. code-block:: yaml

       workspaces:
         temp:
           data_output_dir: /tmp/lorcana-data    # Linux/macOS
           # or
           data_output_dir: C:/temp/lorcana-data  # Windows

2. **Check directory permissions:**

   .. code-block:: shell

       # Linux/macOS
       ls -la data/
       chmod 755 data/
       
       # Windows
       icacls data /grant Everyone:F

3. **Use user home directory:**

   .. code-block:: yaml

       workspaces:
         home:
           data_output_dir: ~/lorcana/data
           image_output_dir: ~/lorcana/images

Disk Space Issues
----------------

**Problem:**

.. code-block:: text

    Error: No space left on device

**Solutions:**

1. **Check disk space:**

   .. code-block:: shell

       # Linux/macOS
       df -h
       
       # Windows
       dir

2. **Use smaller images:**

   .. code-block:: shell

       # Download small images instead of large
       inkcollector lorcast get-cards --set-id TFC --get-images small

3. **Clean up old data:**

   .. code-block:: shell

       # Remove old downloads
       rm -rf data/lorcast/sets/old-set-data
       rm -rf images/lorcast/sets/old-images

4. **Use external storage:**

   .. code-block:: yaml

       workspaces:
         external:
           data_output_dir: /external-drive/lorcana/data
           image_output_dir: /external-drive/lorcana/images

Path Issues
----------

**Problem:**

.. code-block:: text

    Error: Invalid characters in file path

**Solutions:**

1. **Avoid special characters in paths:**

   .. code-block:: yaml

       # Good
       data_output_dir: data/lorcana
       
       # Problematic
       data_output_dir: "data/lorcana & more!/files"

2. **Use forward slashes:**

   .. code-block:: yaml

       # Works on all platforms
       data_output_dir: data/lorcana
       
       # Windows-specific (not recommended)
       data_output_dir: data\lorcana

3. **Use absolute paths when needed:**

   .. code-block:: yaml

       # Absolute paths (adjust for your system)
       data_output_dir: /home/user/lorcana/data      # Linux
       data_output_dir: C:/Users/user/lorcana/data   # Windows

Command Line Issues
==================

Command Not Found
-----------------

**Problem:**

.. code-block:: text

    inkcollector: command not found

**Solutions:**

1. **Check if installed:**

   .. code-block:: shell

       pip list | grep inkcollector

2. **Reinstall:**

   .. code-block:: shell

       pip install --force-reinstall inkcollector

3. **Use full Python path:**

   .. code-block:: shell

       python -m inkcollector --version

4. **Check PATH environment:**

   The pip installation directory must be in your PATH

Argument Errors
--------------

**Problem:**

.. code-block:: text

    Error: unrecognized arguments: --invalid-option

**Solutions:**

1. **Check command syntax:**

   .. code-block:: shell

       inkcollector --help
       inkcollector lorcast --help

2. **Common mistakes:**

   .. code-block:: shell

       # Correct
       inkcollector lorcast get-cards --set-id TFC
       
       # Incorrect
       inkcollector lorcast get-cards --set_id TFC  # underscore instead of hyphen

3. **Global vs command options:**

   .. code-block:: shell

       # Global options go before the command
       inkcollector --profile preview lorcast get-sets
       
       # Not after
       inkcollector lorcast get-sets --profile preview  # Won't work

Performance Issues
=================

Slow Downloads
-------------

**Problem:**

Large image downloads taking too long.

**Solutions:**

1. **Use smaller image sizes:**

   .. code-block:: shell

       # Use small images for faster downloads
       inkcollector lorcast get-cards --set-id TFC --get-images small

2. **Download data separately:**

   .. code-block:: shell

       # Get JSON data first (fast)
       inkcollector --profile data-only lorcast get-cards --set-id TFC
       
       # Download images later when convenient
       inkcollector --profile images-only lorcast get-cards --set-id TFC --get-images

3. **Check network speed:**

   Large sets can have 200+ cards with multiple MB per image

Memory Issues
------------

**Problem:**

.. code-block:: text

    MemoryError: Unable to allocate memory

**Solutions:**

1. **Process smaller sets:**

   Instead of downloading everything at once, process sets individually

2. **Use data-only profile:**

   .. code-block:: shell

       # JSON data uses much less memory than images
       inkcollector --profile data-only lorcast get-cards --set-id TFC

3. **Restart between large operations:**

   Clear memory between large downloads

Debug Mode
==========

Getting More Information
-----------------------

**Enable verbose output:**

While Inkcollector doesn't have a built-in debug mode, you can get more information:

1. **Use preview profile:**

   .. code-block:: shell

       # See exactly what data is being fetched
       inkcollector --profile preview lorcast get-sets

2. **Check configuration:**

   .. code-block:: shell

       # Verify your current settings
       inkcollector config show

3. **Test connectivity:**

   .. code-block:: shell

       # Test basic API access
       curl https://api.lorcast.com/v0/sets

Reporting Issues
===============

When to Report
-------------

Report issues when:

- Commands consistently fail with error messages
- Data appears corrupted or incomplete
- New API errors occur
- Documentation is unclear or incorrect

What to Include
--------------

When reporting issues, include:

1. **Inkcollector version:**

   .. code-block:: shell

       inkcollector --version

2. **Command that failed:**

   .. code-block:: shell

       inkcollector --profile preview lorcast get-sets

3. **Complete error message:**

   Copy the full error output

4. **Configuration file:**

   .. code-block:: shell

       inkcollector config show

5. **Environment details:**

   - Operating system
   - Python version
   - Network environment (corporate, home, etc.)

Where to Report
--------------

- **GitHub Issues:** https://github.com/bertcafecito/inkcollector/issues
- **Include:** Version, command, error message, configuration

Common Solutions Summary
=======================

Quick Reference
--------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Problem Type
     - Quick Solution
   * - Installation fails
     - Use virtual environment: ``python -m venv env && source env/bin/activate``
   * - Command not found
     - Check installation: ``pip list | grep inkcollector``
   * - Config file missing
     - Create one: ``inkcollector config init``
   * - Invalid profile
     - List available: ``inkcollector config list --profiles``
   * - API connection fails
     - Test connectivity: ``inkcollector --profile preview lorcast get-sets``
   * - Set ID not found
     - Check available: ``inkcollector --profile preview lorcast get-sets``
   * - Permission denied
     - Use different directory or fix permissions
   * - Disk space full
     - Use smaller images: ``--get-images small``
   * - Downloads slow
     - Get data first: ``--profile data-only``, then images separately

Prevention Tips
==============

Best Practices
--------------

1. **Always use virtual environments**
2. **Test with preview profile first**
3. **Start with small operations**
4. **Keep configuration files in version control**
5. **Monitor disk space before large downloads**
6. **Use meaningful workspace names**
7. **Backup important data regularly**

Regular Maintenance
------------------

1. **Update Inkcollector regularly:**

   .. code-block:: shell

       pip install --upgrade inkcollector

2. **Clean up old data periodically**

3. **Verify configuration after updates:**

   .. code-block:: shell

       inkcollector config show

4. **Test critical workflows periodically**

Next Steps
==========

If you're still having issues:

1. Check the :doc:`examples` for working configurations
2. Review the :doc:`cli-reference` for correct command syntax
3. Consult the :doc:`configuration` guide for setup help
4. Report persistent issues on `GitHub <https://github.com/bertcafecito/inkcollector/issues>`_
