.. _changelog:

=========
Changelog
=========

All notable changes to Inkcollector are documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

[Unreleased]
============

Nothing yet.

[1.1.0] - 2025-01-15
====================

This major update introduces comprehensive configuration file support, making Inkcollector much more flexible and powerful for different workflows.

Added
-----

**Configuration System:**
- YAML configuration file support (``.inkcollector.yaml``)
- Automatic configuration file discovery (current and parent directories)
- ``config init`` command to create default configuration files
- ``config show`` command to display current configuration  
- ``config list`` command to list available profiles and workspaces

**Extraction Profiles:**
- ``complete`` profile - Extract all data and images (default)
- ``images-only`` profile - Download only card images
- ``data-only`` profile - Extract only JSON data  
- ``preview`` profile - Show data in console without saving files
- Support for custom profiles in configuration files

**Workspace Management:**
- Configurable output directories for data and images
- Multiple workspace support for different projects/environments
- Default workspace with standard directory structure
- Custom workspace definitions in configuration files

**Global Options:**
- ``--config PATH`` - Specify custom configuration file
- ``--workspace NAME`` - Override workspace selection
- ``--profile NAME`` - Override profile selection
- Global options work with all commands

**Enhanced CLI:**
- Improved command structure and help messages
- Better error messages and user feedback
- Configuration validation and helpful suggestions
- Consistent option naming and behavior

Changed
-------

**Command Behavior:**
- Commands now respect configuration profiles by default
- Output directories are configurable via workspaces
- CLI flags (``--json``, ``--save-json``, ``--get-images``) override profile settings
- Better integration between configuration and command-line options

**Directory Structure:**
- Default structure remains the same for backward compatibility
- Configurable via workspace settings
- Automatic directory creation for all configured paths

**Error Handling:**
- More descriptive error messages
- Configuration-specific error guidance
- Better handling of missing profiles/workspaces

Improved
--------

**Documentation:**
- Comprehensive documentation rewrite
- Separate guides for installation, configuration, and usage
- Real-world examples and workflows
- Troubleshooting guide with common solutions
- API integration technical documentation

**User Experience:**
- Streamlined workflow for common tasks
- Easier setup with ``config init`` command
- Clear separation between exploration and production workflows
- Better default behaviors

**Code Quality:**
- Improved error handling and validation
- Better separation of concerns
- Enhanced test coverage
- Code style improvements

[1.0.0] - 2024-12-01
====================

Initial release of Inkcollector with core functionality.

Added
-----

**Core Features:**
- ``lorcast get-sets`` command to fetch all Disney Lorcana card sets
- ``lorcast get-cards`` command to fetch cards for specific sets
- Card image downloading in multiple sizes (small, normal, large)
- JSON data export with optional console display
- Automatic directory structure creation

**CLI Interface:**
- Comprehensive command-line interface using argparse
- ``--json`` flag for console JSON output
- ``--save-json`` flag for file saving
- ``--get-images [SIZE]`` flag for image downloading
- ``--set-id`` required argument for card commands

**API Integration:**
- Integration with Lorcast API (https://api.lorcast.com/v0)
- Support for sets and cards endpoints
- HTTP error handling and retries
- Comprehensive data extraction

**Data Management:**
- Structured JSON file storage
- Organized image file storage by set
- Automatic file naming conventions
- Progress reporting for downloads

**Error Handling:**
- Network error handling
- API error responses
- File system error handling
- User-friendly error messages

**Development:**
- Complete test suite with pytest
- Code formatting with Black
- Import sorting with isort
- Linting with flake8
- Comprehensive development documentation

Technical Details
================

Dependencies
-----------

**Runtime Dependencies:**
- ``requests>=2.32.3`` - HTTP client for API communication
- ``PyYAML>=6.0`` - YAML parser for configuration files

**Development Dependencies:**  
- ``pytest>=7.0.0`` - Testing framework
- ``pytest-mock>=3.10.0`` - Mocking for tests
- ``pytest-cov>=4.0.0`` - Test coverage reporting
- ``black>=23.0.0`` - Code formatting
- ``isort>=5.12.0`` - Import sorting
- ``flake8>=6.0.0`` - Code linting

**Documentation Dependencies:**
- ``Sphinx>=8.2.3`` - Documentation generation
- ``sphinx-rtd-theme>=3.0.2`` - Read the Docs theme

Supported Platforms
------------------

- **Python:** 3.9+ 
- **Operating Systems:** Windows, macOS, Linux
- **Architectures:** x86_64, ARM64

API Compatibility
----------------

- **Lorcast API:** v0
- **Supported Endpoints:**
  - ``/sets`` - All card sets
  - ``/sets/{id}`` - Specific set information
  - ``/sets/{id}/cards`` - Cards for specific set

Migration Guide
==============

From 1.0.x to 1.1.0
-------------------

**Backward Compatibility:**

Inkcollector 1.1.0 is fully backward compatible. All existing commands work exactly as before.

**Optional Migration:**

To take advantage of new features:

1. **Create a configuration file:**

   .. code-block:: shell

       inkcollector config init

2. **Customize for your workflow:**

   Edit ``.inkcollector.yaml`` to define custom profiles and workspaces.

3. **Use new global options:**

   .. code-block:: shell

       # Old way (still works)
       inkcollector lorcast get-sets --json --save-json
       
       # New way with profiles
       inkcollector --profile preview lorcast get-sets

**Breaking Changes:**

None. All existing commands and options continue to work.

Known Issues
===========

Current Limitations
------------------

- Configuration files must be in YAML format
- Profile and workspace names are case-sensitive
- Image downloads are sequential (no parallel downloading)
- No built-in rate limiting for API requests

Planned Improvements
-------------------

**Future Releases:**
- Parallel image downloading for better performance
- Additional output formats (CSV, XML)
- Built-in rate limiting and retry strategies
- Plugin system for custom data processors
- Advanced filtering and search capabilities

**Under Consideration:**
- GUI interface for non-technical users
- Integration with other Disney Lorcana data sources
- Caching layer for improved performance
- Batch processing capabilities

Contributing
===========

Inkcollector is open source and welcomes contributions!

**Ways to Contribute:**
- Report bugs and issues
- Suggest new features
- Improve documentation
- Submit code improvements
- Help other users

**Getting Started:**
- See :doc:`contributing` for detailed guidelines
- Check `GitHub Issues <https://github.com/bertcafecito/inkcollector/issues>`_ for open tasks
- Join discussions in `GitHub Discussions <https://github.com/bertcafecito/inkcollector/discussions>`_

Credits
=======

**Author:** Bert Cafecito

**Contributors:**
- Community feedback and bug reports
- Documentation improvements
- Feature suggestions

**Special Thanks:**
- Lorcast API for providing Disney Lorcana data
- Disney for creating the amazing Lorcana trading card game
- The Python community for excellent tools and libraries

**Open Source Libraries:**
- `requests <https://docs.python-requests.org/>`_ - HTTP library
- `PyYAML <https://pyyaml.org/>`_ - YAML parser
- `pytest <https://pytest.org/>`_ - Testing framework
- `Sphinx <https://www.sphinx-doc.org/>`_ - Documentation generation

License
=======

Inkcollector is released under the `MIT License <https://github.com/bertcafecito/inkcollector/blob/main/LICENSE>`_.

This means you can:
- Use it for any purpose (commercial or personal)
- Modify and distribute it
- Include it in proprietary software

The only requirement is to include the original copyright notice.

**Disclaimer:** Inkcollector is not affiliated with Disney or the official Lorcana trading card game. It's a community tool for accessing publicly available data.
