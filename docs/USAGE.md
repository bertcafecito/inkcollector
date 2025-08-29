# Inkcollector Usage Guide

This guide provides comprehensive usage instructions for the Inkcollector CLI tool.

## Table of Contents

- [Getting Started](#getting-started)
- [Global Options](#global-options)
- [Command Reference](#command-reference)
- [Configuration Commands](#configuration-commands)
- [Lorcast Commands](#lorcast-commands)
- [Profile Examples](#profile-examples)
- [Migration Guide](#migration-guide)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Installation

```bash
pip install inkcollector
```

### Basic Commands

```bash
# Check version
inkcollector --version

# Get help
inkcollector --help

# Basic data collection
inkcollector lorcast get-sets
```

### First-time Configuration

```bash
# Create a configuration file
inkcollector config init

# View your configuration
inkcollector config show

# List available profiles and workspaces
inkcollector config list
```

## Global Options

All commands support these global options:

- `--config PATH`: Specify custom configuration file
- `--workspace NAME`: Override workspace selection
- `--profile NAME`: Override profile selection
- `--version`: Show version information
- `--help`: Show help message

### Examples

```bash
# Use custom config file
inkcollector --config my-config.yaml lorcast get-sets

# Override workspace
inkcollector --workspace research lorcast get-sets

# Override profile
inkcollector --profile preview lorcast get-sets

# Combine multiple overrides
inkcollector --config my-config.yaml --workspace collection --profile high-quality lorcast get-cards --set-id set_123
```

## Command Reference

### Configuration Commands

#### `config init`

Create a sample configuration file.

```bash
# Create default configuration file
inkcollector config init

# Create configuration at custom path
inkcollector config init --path my-config.yaml

# Overwrite existing configuration
inkcollector config init --force
```

**Options:**
- `--path PATH`: Specify configuration file path (default: `.inkcollector.yaml`)
- `--force`: Overwrite existing configuration file

#### `config show`

Display current configuration.

```bash
# Show current configuration (YAML format)
inkcollector config show

# Show configuration in JSON format
inkcollector config show --format json
```

**Options:**
- `--format FORMAT`: Output format (`yaml` or `json`, default: `yaml`)

#### `config list`

List available profiles and workspaces.

```bash
# List all profiles and workspaces
inkcollector config list

# List only profiles
inkcollector config list --profiles

# List only workspaces
inkcollector config list --workspaces
```

**Options:**
- `--profiles`: List only extraction profiles
- `--workspaces`: List only workspace configurations

### Lorcast Commands

The `lorcast` command group provides access to the Lorcast API for Disney Lorcana data collection.

#### `lorcast get-sets`

Retrieve all available Disney Lorcana card sets.

```bash
# Basic usage (respects active profile)
inkcollector lorcast get-sets

# Force console output
inkcollector lorcast get-sets --json

# Force file saving
inkcollector lorcast get-sets --save-json

# Both console and file output
inkcollector lorcast get-sets --json --save-json
```

**Options:**
- `--json`: Print JSON data to console (overrides profile setting)
- `--save-json`: Save JSON data to file (overrides profile setting)

**Behavior:**
- Fetches all available sets from the Lorcast API
- Respects active extraction profile settings
- Creates necessary output directories automatically
- Displays number of sets found

#### `lorcast get-cards`

Retrieve detailed card information for a specific set.

```bash
# Basic usage
inkcollector lorcast get-cards --set-id set_c64f092e725a4f66966f43af3aa161b6

# With console output
inkcollector lorcast get-cards --set-id set_123 --json

# With file saving
inkcollector lorcast get-cards --set-id set_123 --save-json

# Download images (normal size)
inkcollector lorcast get-cards --set-id set_123 --get-images

# Download images (specific size)
inkcollector lorcast get-cards --set-id set_123 --get-images large

# Complete workflow
inkcollector lorcast get-cards --set-id set_123 --json --save-json --get-images normal
```

**Required Arguments:**
- `--set-id SET_ID`: ID of the card set to retrieve cards from

**Options:**
- `--json`: Print JSON card data to console (overrides profile setting)
- `--save-json`: Save card data to file (overrides profile setting)
- `--get-images [SIZE]`: Download card images with specified size
  - Available sizes: `small`, `normal`, `large`
  - Default size: `normal` (if no size specified)

**Behavior:**
- Validates set ID by fetching set information first
- Retrieves all cards for the specified set
- Respects active extraction profile settings
- Downloads card images based on profile or command options
- Creates necessary output directories automatically
- Reports download statistics for images

## Profile Examples

### Default Profiles

Inkcollector includes four built-in profiles:

#### 1. `complete` (default)
Extract all data and images with normal image size.
```bash
inkcollector --profile complete lorcast get-cards --set-id set_123
```

#### 2. `images-only`
Extract only card images, no JSON data.
```bash
inkcollector --profile images-only lorcast get-cards --set-id set_123
```

#### 3. `data-only`
Extract only JSON data, no images.
```bash
inkcollector --profile data-only lorcast get-sets
```

#### 4. `preview`
Show data in console without saving files.
```bash
inkcollector --profile preview lorcast get-sets
```

### Custom Profile Usage

Create custom profiles in your `.inkcollector.yaml`:

```yaml
profiles:
  high-quality:
    description: "High-quality images with data"
    extract_data: true
    extract_images: true
    image_size: large
    save_json: true
    print_json: false

  research:
    description: "Research workflow with console output"
    extract_data: true
    extract_images: false
    save_json: true
    print_json: true
```

Use custom profiles:
```bash
inkcollector --profile high-quality lorcast get-cards --set-id set_123
inkcollector --profile research lorcast get-sets
```

### Workspace Examples

Define workspaces for different environments:

```yaml
workspaces:
  development:
    data_output_dir: dev/data
    image_output_dir: dev/images
    default_profile: preview

  production:
    data_output_dir: prod/data
    image_output_dir: prod/images
    default_profile: complete

  research:
    data_output_dir: research/data
    image_output_dir: research/images
    default_profile: data-only
```

Use workspaces:
```bash
# Development environment
inkcollector --workspace development lorcast get-sets

# Production environment
inkcollector --workspace production lorcast get-cards --set-id set_123

# Research environment
inkcollector --workspace research lorcast get-sets
```

## Migration Guide

### Configuration File Discovery

Inkcollector automatically searches for `.inkcollector.yaml` in:

1. Current working directory
2. Parent directory
3. Parent's parent directory
4. Parent's parent's parent directory

If no configuration file is found, default settings are used.

### Migrating from CLI-only Usage

**Before (CLI only):**
```bash
inkcollector lorcast get-cards --set-id set_123 --save-json --get-images normal
```

**After (with configuration):**

1. Create a profile in `.inkcollector.yaml`:
```yaml
profiles:
  my-profile:
    description: "My usual settings"
    extract_data: true
    extract_images: true
    image_size: normal
    save_json: true
    print_json: false
```

2. Use the profile:
```bash
inkcollector --profile my-profile lorcast get-cards --set-id set_123
```

### Backward Compatibility

All existing CLI commands continue to work exactly as before:

- Configuration files are optional
- CLI arguments always take precedence over configuration settings
- Default behavior remains unchanged when no configuration is present

## Directory Structure

### Default Structure

Inkcollector creates the following directory structure by default:

```
data/
├── lorcast/
│   ├── sets.json
│   └── sets/
│       └── <set_id>.json
images/
└── lorcast/
    └── sets/
        └── <set_id>/
            └── crd_<card_id>.jpg
```

### Custom Structure

Configure custom directories using workspaces:

```yaml
workspaces:
  custom:
    data_output_dir: my_data
    image_output_dir: my_images
```

Results in:
```
my_data/
├── lorcast/
│   ├── sets.json
│   └── sets/
│       └── <set_id>.json
my_images/
└── lorcast/
    └── sets/
        └── <set_id>/
            └── crd_<card_id>.jpg
```

## Priority Order

Configuration settings are applied in this order (highest to lowest priority):

1. **Command line arguments** (e.g., `--json`, `--save-json`, `--get-images`)
2. **Profile settings** specified with `--profile`
3. **Default profile** from active workspace
4. **Default profile** from configuration file
5. **Built-in defaults**

## Troubleshooting

### Common Issues

#### Configuration file not found
```bash
# Check current directory for .inkcollector.yaml
ls -la .inkcollector.yaml

# Create new configuration
inkcollector config init

# Use specific config file
inkcollector --config path/to/config.yaml lorcast get-sets
```

#### Profile not found
```bash
# List available profiles
inkcollector config list --profiles

# Check profile name in configuration
inkcollector config show
```

#### Permission errors
```bash
# Check directory permissions
ls -la data/ images/

# Use different output directories
inkcollector --workspace custom lorcast get-sets
```

#### Network errors
```bash
# Check internet connection
ping api.lorcast.com

# Retry with specific set ID
inkcollector lorcast get-cards --set-id set_123
```

### Debug Information

To get more detailed information:

```bash
# Show current configuration
inkcollector config show

# List all available options
inkcollector config list

# Use preview profile to test without saving files
inkcollector --profile preview lorcast get-sets
```

### Getting Help

```bash
# Main help
inkcollector --help

# Command-specific help
inkcollector lorcast --help
inkcollector config --help

# Subcommand help
inkcollector lorcast get-cards --help
inkcollector config init --help
```

For additional support:
- 📖 [Configuration Documentation](CONFIG.md)
- 🐛 [Report Issues](https://github.com/bertcafecito/inkcollector/issues)
- 📚 [Full Documentation](https://bertcafecito.github.io/inkcollector/)
