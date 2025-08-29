# Inkcollector Documentation

Welcome to the Inkcollector documentation! This directory contains comprehensive guides and references for using the Inkcollector CLI tool.

## 📚 Documentation Overview

### Quick Navigation

- **[Usage Guide](USAGE.md)** - Complete usage instructions and command reference
- **[Configuration Guide](CONFIG.md)** - YAML configuration system documentation  
- **[API Documentation](source/index.rst)** - Detailed API and technical documentation

### Getting Started

1. **Installation**: See the main [README](../README.md) for installation instructions
2. **First Steps**: Start with the [Usage Guide](USAGE.md#getting-started)
3. **Configuration**: Learn about profiles and workspaces in the [Configuration Guide](CONFIG.md)

## 📖 Documentation Structure

### [USAGE.md](USAGE.md)
Comprehensive usage guide covering:
- Getting started and basic commands
- Global options and command reference
- Configuration commands (`config init`, `show`, `list`)
- Lorcast commands (`get-sets`, `get-cards`)
- Profile and workspace examples
- Migration guide from CLI-only usage
- Troubleshooting tips

### [CONFIG.md](CONFIG.md)
Configuration system documentation covering:
- Configuration file structure and creation
- Extraction profiles (complete, images-only, data-only, preview)
- Workspace configurations for different environments
- Custom profile and workspace creation
- Configuration priority and inheritance
- Advanced configuration examples

### [source/index.rst](source/index.rst)
Technical documentation including:
- API integration details
- Class and method documentation
- Technical implementation details
- Sphinx-generated documentation

## 🚀 Quick Reference

### Essential Commands

```bash
# Installation
pip install inkcollector

# Basic usage
inkcollector lorcast get-sets

# Configuration setup
inkcollector config init
inkcollector config show
inkcollector config list

# Profile usage
inkcollector --profile preview lorcast get-sets
inkcollector --profile images-only lorcast get-cards --set-id set_123

# Workspace usage
inkcollector --workspace research lorcast get-sets
```

### Configuration File Example

```yaml
default_workspace: default
api_base_url: https://api.lorcast.com
api_version: v0

profiles:
  my-profile:
    description: "Custom extraction profile"
    extract_data: true
    extract_images: true
    image_size: large
    save_json: true
    print_json: false

workspaces:
  research:
    data_output_dir: research/data
    image_output_dir: research/images
    default_profile: data-only
```

## 🔗 External Links

- **[GitHub Repository](https://github.com/bertcafecito/inkcollector)** - Source code and issues
- **[PyPI Package](https://pypi.org/project/inkcollector/)** - Package information and downloads
- **[Lorcast API](https://lorcast.com/docs/api)** - Official Lorcast API documentation

## 🆘 Getting Help

If you need help:

1. **Check the documentation** - Most questions are answered in [USAGE.md](USAGE.md) or [CONFIG.md](CONFIG.md)
2. **Search existing issues** - [GitHub Issues](https://github.com/bertcafecito/inkcollector/issues)
3. **Report a bug** - [Create a new issue](https://github.com/bertcafecito/inkcollector/issues/new)
4. **Ask for help** - [Start a discussion](https://github.com/bertcafecito/inkcollector/discussions)

## 📝 Contributing to Documentation

Found an error or want to improve the documentation? 

1. Fork the repository
2. Edit the relevant documentation file
3. Submit a pull request

Documentation files use Markdown (`.md`) format for easy editing.
