.. _contributing:

============
Contributing
============

Thank you for your interest in contributing to Inkcollector! This guide will help you get started.

Getting Started
===============

Development Setup
----------------

1. **Fork and clone the repository:**

   .. code-block:: shell

       git clone https://github.com/YOUR-USERNAME/inkcollector.git
       cd inkcollector

2. **Create a virtual environment:**

   .. code-block:: shell

       python -m venv venv
       
       # Activate it
       # Windows
       venv\Scripts\activate
       # macOS/Linux
       source venv/bin/activate

3. **Install in development mode:**

   .. code-block:: shell

       # Install the package in development mode
       pip install -e .
       
       # Install development dependencies
       pip install -e ".[dev,docs]"

4. **Verify installation:**

   .. code-block:: shell

       inkcollector --version
       pytest --version

Project Structure
================

Understanding the codebase:

.. code-block:: text

    inkcollector/
    ├── inkcollector/           # Main package
    │   ├── __init__.py
    │   ├── __main__.py         # Entry point (python -m inkcollector)
    │   ├── cli.py              # CLI interface and argument parsing
    │   ├── config.py           # Configuration management
    │   └── lorcast.py          # Lorcast API integration
    ├── tests/                  # Test suite
    │   ├── test_cli.py
    │   ├── test_config.py
    │   └── conftest.py
    ├── docs/                   # Documentation
    │   ├── source/
    │   └── README.md
    ├── pyproject.toml          # Project configuration
    └── README.md

Key Components
--------------

**CLI Module (cli.py):**
   - Argument parsing with argparse
   - Command routing and execution
   - Global option handling
   - Error message formatting

**Configuration Module (config.py):**
   - YAML configuration file parsing
   - Profile and workspace management
   - Configuration validation
   - Default settings

**Lorcast Module (lorcast.py):**
   - API client implementation
   - HTTP request handling
   - Response processing
   - Image downloading

Running Tests
=============

Test Suite
----------

Run the full test suite:

.. code-block:: shell

    # Run all tests
    pytest
    
    # Run with coverage
    pytest --cov=inkcollector
    
    # Run specific test file
    pytest tests/test_cli.py
    
    # Run specific test
    pytest tests/test_config.py::test_config_creation

Test Categories
--------------

**Unit Tests:**
   - Test individual functions and methods
   - Mock external dependencies (API calls, file system)
   - Fast execution

**Integration Tests:**
   - Test component interactions
   - May use temporary files
   - Slower execution

**CLI Tests:**
   - Test command-line interface
   - Argument parsing validation
   - Error message verification

Writing Tests
------------

**Test Structure:**

.. code-block:: python

    import pytest
    from unittest.mock import patch, mock_open
    from inkcollector.config import ConfigManager

    def test_config_loading():
        """Test configuration file loading."""
        # Arrange
        config_content = """
        default_workspace: test
        profiles:
          test-profile:
            extract_data: true
        """
        
        # Act
        with patch("builtins.open", mock_open(read_data=config_content)):
            config = ConfigManager.load_config("test-config.yaml")
        
        # Assert
        assert config["default_workspace"] == "test"
        assert "test-profile" in config["profiles"]

**Testing Guidelines:**

- Use descriptive test names
- Follow Arrange-Act-Assert pattern
- Mock external dependencies
- Test both success and error cases
- Include edge cases

Code Style
==========

Formatting
----------

Inkcollector uses several tools to maintain code quality:

.. code-block:: shell

    # Format code with black
    black inkcollector/ tests/
    
    # Sort imports with isort
    isort inkcollector/ tests/
    
    # Check style with flake8
    flake8 inkcollector/ tests/

**Pre-commit Setup:**

.. code-block:: shell

    # Install pre-commit hooks (optional)
    pip install pre-commit
    pre-commit install

Style Guidelines
---------------

**Code Formatting:**
   - Use Black for automatic formatting
   - Maximum line length: 88 characters
   - Use double quotes for strings

**Imports:**
   - Sort with isort
   - Group: standard library, third-party, local
   - Use absolute imports

**Naming Conventions:**
   - Functions and variables: ``snake_case``
   - Classes: ``PascalCase``
   - Constants: ``UPPER_CASE``
   - Private methods: ``_leading_underscore``

**Documentation:**
   - Use docstrings for public functions
   - Follow Google docstring format
   - Include type hints where helpful

**Example:**

.. code-block:: python

    def download_card_images(
        cards_data: dict, 
        output_dir: str, 
        image_size: str = "normal"
    ) -> tuple[int, int]:
        """Download card images from API response.
        
        Args:
            cards_data: API response containing card information
            output_dir: Directory to save images
            image_size: Size of images to download (small/normal/large)
            
        Returns:
            Tuple of (successful_downloads, total_cards)
            
        Raises:
            ValueError: If image_size is not valid
            OSError: If output directory cannot be created
        """
        pass

Documentation
=============

Building Documentation
---------------------

.. code-block:: shell

    # Install documentation dependencies
    pip install -e ".[docs]"
    
    # Build HTML documentation
    cd docs
    make html
    
    # On Windows
    make.bat html
    
    # View documentation
    open _build/html/index.html

Documentation Guidelines
-----------------------

**Sphinx Documentation:**
   - Write in reStructuredText format
   - Use clear section headers
   - Include code examples
   - Cross-reference other sections

**Docstrings:**
   - Use Google style docstrings
   - Document all public functions
   - Include examples for complex functions

**Examples:**

.. code-block:: rst

    Example Section
    ===============
    
    Brief description of what this section covers.
    
    Basic Usage
    -----------
    
    .. code-block:: shell
    
        # Example command
        inkcollector lorcast get-sets
    
    See :doc:`cli-reference` for more details.

Contributing Guidelines
======================

Types of Contributions
---------------------

**Bug Reports:**
   - Use GitHub Issues
   - Include version information
   - Provide reproduction steps
   - Include error messages

**Feature Requests:**
   - Describe the problem you're solving
   - Propose a solution approach
   - Consider backward compatibility

**Code Contributions:**
   - Start with an issue or discussion
   - Create feature branch
   - Write tests
   - Update documentation

**Documentation:**
   - Fix typos and unclear sections
   - Add examples and use cases
   - Improve existing explanations

Pull Request Process
-------------------

1. **Create a branch:**

   .. code-block:: shell

       git checkout -b feature/add-new-feature
       # or
       git checkout -b bugfix/fix-config-issue

2. **Make your changes:**

   - Write code following style guidelines
   - Add or update tests
   - Update documentation if needed

3. **Test your changes:**

   .. code-block:: shell

       # Run tests
       pytest
       
       # Check code style
       black --check inkcollector/ tests/
       flake8 inkcollector/ tests/
       
       # Build documentation
       cd docs && make html

4. **Commit your changes:**

   .. code-block:: shell

       git add .
       git commit -m "Add support for custom API endpoints"

5. **Push and create PR:**

   .. code-block:: shell

       git push origin feature/add-new-feature

6. **Create Pull Request:**

   - Use descriptive title
   - Explain what changes you made
   - Link to related issues
   - Include testing information

Commit Message Guidelines
------------------------

**Format:**

.. code-block:: text

    type(scope): brief description
    
    Longer explanation if needed
    
    Fixes #123

**Types:**
   - ``feat``: New feature
   - ``fix``: Bug fix
   - ``docs``: Documentation changes
   - ``style``: Code style changes
   - ``refactor``: Code refactoring
   - ``test``: Adding or updating tests
   - ``chore``: Maintenance tasks

**Examples:**

.. code-block:: text

    feat(config): add support for custom API endpoints
    
    fix(cli): handle missing set ID error gracefully
    
    docs(readme): update installation instructions
    
    test(config): add tests for YAML validation

Code Review Process
==================

What We Look For
---------------

**Code Quality:**
   - Follows style guidelines
   - Includes appropriate tests
   - Has clear documentation
   - Handles errors gracefully

**Functionality:**
   - Solves the intended problem
   - Doesn't break existing features
   - Works on supported platforms
   - Has reasonable performance

**Design:**
   - Fits with existing architecture
   - Maintains backward compatibility
   - Uses appropriate abstractions
   - Follows project conventions

Review Guidelines
----------------

**For Contributors:**
   - Be open to feedback
   - Explain design decisions
   - Update based on suggestions
   - Keep commits focused

**For Reviewers:**
   - Be constructive and helpful
   - Explain reasoning for suggestions
   - Acknowledge good work
   - Focus on significant issues

Development Tips
===============

Debugging
--------

**Debug Configuration Issues:**

.. code-block:: python

    # Add debug prints to config.py
    def load_config(config_path):
        print(f"Loading config from: {config_path}")
        with open(config_path) as f:
            data = yaml.safe_load(f)
        print(f"Loaded data: {data}")
        return data

**Debug API Issues:**

.. code-block:: python

    # Add debug prints to lorcast.py
    def make_request(url):
        print(f"Making request to: {url}")
        response = requests.get(url)
        print(f"Response status: {response.status_code}")
        return response

**Use pytest for interactive debugging:**

.. code-block:: shell

    # Drop into debugger on failure
    pytest --pdb
    
    # Drop into debugger immediately
    pytest --pdb -s tests/test_specific.py::test_function

Testing Strategies
-----------------

**Mock External Dependencies:**

.. code-block:: python

    @patch('inkcollector.lorcast.requests.get')
    def test_api_call(mock_get):
        # Arrange
        mock_response = Mock()
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response
        
        # Act
        result = api_client.get_sets()
        
        # Assert
        assert result == {"results": []}
        mock_get.assert_called_once()

**Test File Operations:**

.. code-block:: python

    def test_config_save(tmp_path):
        # Use pytest's tmp_path fixture
        config_file = tmp_path / "test-config.yaml"
        config_data = {"default_workspace": "test"}
        
        save_config(config_data, config_file)
        
        assert config_file.exists()
        loaded = load_config(config_file)
        assert loaded == config_data

Release Process
==============

Version Management
-----------------

Inkcollector uses semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR:** Breaking changes
- **MINOR:** New features (backward compatible)
- **PATCH:** Bug fixes

**Update Version:**

1. Update ``pyproject.toml``
2. Update ``__init__.py`` if applicable
3. Update documentation references
4. Create release notes

Community
=========

Communication
------------

**GitHub Discussions:**
   - Feature discussions
   - Usage questions
   - Community feedback

**GitHub Issues:**
   - Bug reports
   - Feature requests
   - Documentation issues

**Code of Conduct:**
   - Be respectful and inclusive
   - Focus on constructive feedback
   - Help others learn and grow

Getting Help
-----------

**For Development Questions:**
   - Check existing issues and discussions
   - Review documentation and examples
   - Ask specific, detailed questions

**For Complex Changes:**
   - Open an issue to discuss approach
   - Consider breaking into smaller changes
   - Ask for feedback early in the process

Thank You!
==========

Your contributions help make Inkcollector better for everyone. Whether you're fixing bugs, adding features, improving documentation, or helping other users, your efforts are appreciated!

Key Points to Remember:

- Start small and build up
- Ask questions when uncertain  
- Follow the style guidelines
- Write tests for your changes
- Update documentation as needed
- Be patient with the review process

Happy contributing! 🎉
