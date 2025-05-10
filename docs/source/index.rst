.. inkcollector documentation master file, created by
   sphinx-quickstart on Sat May 10 00:25:58 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

inkcollector documentation
==========================

Welcome to the Inkcollector documentation! Inkcollector is a command-line interface (CLI) tool designed to collect data about the Disney Lorcana trading card game.

## CLI Overview

Inkcollector provides a simple and intuitive CLI interface to interact with Disney Lorcana card data. Below is a detailed guide to the available commands and options.

## Commands

### `inkcollector`

The main entry point for the CLI. Run this command to start using Inkcollector.

```bash
inkcollector
```

### `inkcollector --help`

Displays help information about the available commands and options.

```bash
inkcollector --help
```

### `inkcollector fetch`

Fetches the latest Disney Lorcana card data from the official source.

```bash
inkcollector fetch
```

#### Options:
- `--output <file>`: Save the fetched data to a specified file.
- `--verbose`: Enable verbose output for debugging purposes.

### `inkcollector list`

Lists all the Disney Lorcana cards currently available in the database.

```bash
inkcollector list
```

#### Options:
- `--filter <criteria>`: Filter the list by specific criteria (e.g., rarity, type).
- `--sort <field>`: Sort the list by a specific field (e.g., name, cost).

### `inkcollector search`

Searches for a specific card by name or other attributes.

```bash
inkcollector search <query>
```

#### Options:
- `--exact`: Perform an exact match search.
- `--fields <fields>`: Specify which fields to search (e.g., name, description).

## Examples

### Fetch and Save Data

```bash
inkcollector fetch --output cards.json
```

### List Cards Sorted by Name

```bash
inkcollector list --sort name
```

### Search for a Card by Name

```bash
inkcollector search "Mickey Mouse"
```

## Development

To set up a development environment, install the optional dependencies for documentation and testing:

```bash
pip install .[docs]
```

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   cli
   api
   development

