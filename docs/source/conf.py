# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import toml
from pathlib import Path

# Load project metadata from pyproject.toml
pyproject_path = Path(__file__).resolve().parents[2] / "pyproject.toml"
pyproject_data = toml.load(pyproject_path)
project_metadata = pyproject_data.get("project", {})

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = project_metadata.get("name", "Unknown Project")
copyright = f"2025, {project_metadata.get('authors', [{'name': 'Unknown Author'}])[0]['name']}"
author = project_metadata.get("authors", [{'name': 'Unknown Author'}])[0]['name']
release = project_metadata.get("version", "0.0.0")

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
