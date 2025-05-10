# Inkcollector

Inkcollector is a command-line interface (CLI) tool designed to collect data about the Disney Lorcana trading card game.

## Features

- Fetch and display information about Disney Lorcana cards.
- Easy-to-use CLI interface powered by [Click](https://click.palletsprojects.com/).
- Extensible and open-source.

## Installation

To install Inkcollector, clone the repository and install the dependencies:

```bash
git clone https://github.com/your-username/inkcollector.git
cd inkcollector
pip install .
```

## Usage

Run the CLI tool using the following command:

```bash
inkcollector
```

For help and available commands, use:

```bash
inkcollector --help
```

## Getting Started

Here is a quick example of how to use Inkcollector to fetch information about a specific card:

```bash
inkcollector fetch-card --name "Mickey Mouse"
```

This will display detailed information about the specified card.

## Development

To set up a development environment, install the optional dependencies for documentation and testing:

```bash
pip install .[docs,dev]
```

### Running Tests

Run the test suite using `pytest`:

```bash
pytest
```

### Code Formatting

Ensure your code is formatted using `black`:

```bash
black .
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and ensure tests pass.
4. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.