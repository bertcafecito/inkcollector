# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-08-28

### Added
- **Image Download Functionality**: Added capability to download card images.
- **JSON Saving Functionality**: Added ability to save Lorcast command outputs to JSON files.
- **JSON Console Output Flag**: Added flag to display JSON output in console for Lorcast subcommands.
- **Comprehensive Testing Suite**: Implemented pytest configuration with coverage reporting.
- **Code Quality Tools**: Added linting and testing to CI workflow.
- **Development Dependencies**: Added black, isort, flake8, pytest, and coverage tools.
- **YAML Issue Templates**: Replaced markdown issue templates with structured YAML forms for better issue reporting.
- **Comprehensive CLI Documentation**: Added detailed documentation for the Inkcollector CLI tool, including features, installation, usage, and examples.
- **AI Assistance Acknowledgment**: Added acknowledgment of AI assistance in development with emphasis on manual review.

### Changed
- **Major CLI Refactor**: Switched to class-based CLI architecture using argparse.
- **Enhanced Lorcast Commands**: Refactored lorcast get-set subcommand for improved functionality.
- **Project Structure**: Reorganized codebase for better maintainability.
- **CLI Improvements**: Enhanced CLI tool with better error messages, improved argument parsing, and enhanced data collection capabilities.
- **Documentation Format**: Migrated README from RST to Markdown format for better compatibility and readability.
- **Code Quality**: Improved error handling, Unicode character support, and file operation error handling.
- **Test Coverage**: Enhanced test cases for CLI functionality with better coverage.

### Removed
- **Legacy CLI Code**: Removed outdated CLI and example code.
- **Development Container**: Removed VSCode development container configuration.
- **Legacy README**: Removed RST format README file in favor of Markdown.

### Updated
- **Version Bump**: Updated to version 1.0.0 marking stable release.
- **Testing Configuration**: Added comprehensive pytest configuration with coverage requirements.
- **CI/CD Pipeline**: Enhanced workflow with linting and testing automation.

## [0.1.1] - 2025-05-11

### Updated
- Updated project documentation for clarity and completeness.

## [0.1.0] - 2025-05-09

### Added

- **Changelog**: Introduced a changelog to document project updates.
- **VSCode Python Devcontainer Configuration**: Added configuration for development environments.
- **CodeQL Analysis Workflow**: Implemented CodeQL workflows for security analysis.
- **CLI Version Display**: Enabled displaying the Inkcollector version via the command line interface.
- **Lorcast Commands**:
  - **Sets Command**: Added command to retrieve Lorcana sets with JSON and CSV output formats.
  - **Cards Command**: Added command to retrieve Lorcana cards with JSON and CSV output formats.
  - **All Command**: Added command to retrieve all Lorcana data with JSON and CSV output formats.
- **Console Logging**: Integrated console logging to enhance debugging capabilities.
- **File Logging**: Implemented file logging for persistent debug information.

[unreleased]: https://github.com/bertcafecito/inkcollector/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/bertcafecito/inkcollector/releases/tag/v1.0.0
[0.1.1]: https://github.com/bertcafecito/inkcollector/releases/tag/v0.1.1
[0.1.0]: https://github.com/bertcafecito/inkcollector/releases/tag/v0.1.0


