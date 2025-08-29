# Configuration System Documentation

Inkcollector supports YAML configuration files that allow you to define default settings, extraction profiles, and workspace configurations. This makes it easy to customize the tool's behavior for different use cases and environments.

## Configuration File

The configuration file is named `.inkcollector.yaml` and should be placed in your project directory. Inkcollector will search for this file in the current directory and up to 3 parent directories.

### Creating a Configuration File

Generate a sample configuration file with all default options:

```bash
inkcollector config init
```

This creates a `.inkcollector.yaml` file with default settings. You can also specify a custom path:

```bash
inkcollector config init --path my-config.yaml
```

### Configuration Structure

The configuration file has four main sections:

```yaml
# Default workspace to use when none is specified
default_workspace: default

# API configuration
api_base_url: https://api.lorcast.com
api_version: v0

# Extraction profiles define what data to extract and how
profiles:
  profile-name:
    description: "Profile description"
    extract_data: true      # Whether to extract JSON data
    extract_images: true    # Whether to download images
    image_size: normal      # Image size: small, normal, large
    save_json: true         # Whether to save JSON to files
    print_json: false       # Whether to print JSON to console

# Workspace configurations define output directories and defaults
workspaces:
  workspace-name:
    data_output_dir: data
    image_output_dir: images
    default_profile: complete
```

## Extraction Profiles

Profiles define what data to extract and how to handle it. Four default profiles are provided:

### Default Profiles

1. **complete** - Extract all data and images (default)
   - Extracts JSON data and saves to files
   - Downloads images in normal size
   - Does not print to console

2. **images-only** - Extract only card images
   - Downloads images in normal size
   - Does not extract or save JSON data

3. **data-only** - Extract only JSON data
   - Extracts JSON data and saves to files
   - Does not download images

4. **preview** - Show data in console without saving
   - Extracts JSON data and prints to console
   - Does not save files or download images

### Custom Profiles

You can create custom profiles in your configuration file:

```yaml
profiles:
  high-quality:
    description: "Extract everything with large images"
    extract_data: true
    extract_images: true
    image_size: large
    save_json: true
    print_json: false

  quick-preview:
    description: "Quick data preview with small images"
    extract_data: true
    extract_images: true
    image_size: small
    save_json: false
    print_json: true
```

## Workspaces

Workspaces define output directories and default settings for different environments or projects.

### Default Workspace

The default workspace uses:
- `data` directory for JSON files
- `images` directory for downloaded images
- `complete` profile as default

### Custom Workspaces

Create custom workspaces for different use cases:

```yaml
workspaces:
  research:
    data_output_dir: research/data
    image_output_dir: research/images
    default_profile: data-only

  collection:
    data_output_dir: collection/data
    image_output_dir: collection/images
    default_profile: high-quality

  development:
    data_output_dir: dev/data
    image_output_dir: dev/images
    default_profile: preview
```

## Using Configuration

### Command Line Options

Override configuration settings using command line options:

```bash
# Use a specific configuration file
inkcollector --config my-config.yaml lorcast get-sets

# Use a specific workspace
inkcollector --workspace research lorcast get-sets

# Use a specific profile
inkcollector --profile preview lorcast get-sets

# Combine options
inkcollector --config my-config.yaml --workspace collection --profile high-quality lorcast get-cards --set-id set_123
```

### Configuration Commands

Manage your configuration using the `config` command:

```bash
# Show current configuration
inkcollector config show

# Show configuration in JSON format
inkcollector config show --format json

# List available profiles and workspaces
inkcollector config list

# List only profiles
inkcollector config list --profiles

# List only workspaces
inkcollector config list --workspaces
```

### Priority Order

Configuration settings are applied in this order (highest to lowest priority):

1. Command line arguments (e.g., `--json`, `--save-json`)
2. Profile settings specified with `--profile`
3. Default profile from workspace
4. Default profile from configuration
5. Built-in defaults

## Examples

### Example 1: Research Setup

Create a configuration for research with data-only extraction:

```yaml
default_workspace: research

workspaces:
  research:
    data_output_dir: research/data
    image_output_dir: research/images
    default_profile: data-only

profiles:
  data-only:
    description: "Extract only JSON data for research"
    extract_data: true
    extract_images: false
    save_json: true
    print_json: false
```

Usage:
```bash
inkcollector lorcast get-sets  # Uses research workspace and data-only profile
```

### Example 2: Multi-Environment Setup

Configure different environments:

```yaml
default_workspace: development

workspaces:
  development:
    data_output_dir: dev/data
    image_output_dir: dev/images
    default_profile: preview

  staging:
    data_output_dir: staging/data
    image_output_dir: staging/images
    default_profile: complete

  production:
    data_output_dir: prod/data
    image_output_dir: prod/images
    default_profile: high-quality

profiles:
  preview:
    description: "Development preview"
    extract_data: true
    extract_images: false
    save_json: false
    print_json: true

  high-quality:
    description: "Production quality"
    extract_data: true
    extract_images: true
    image_size: large
    save_json: true
    print_json: false
```

Usage:
```bash
# Development (default)
inkcollector lorcast get-sets

# Staging
inkcollector --workspace staging lorcast get-sets

# Production
inkcollector --workspace production lorcast get-sets
```

### Example 3: Profile Override

Use different profiles with the same workspace:

```bash
# Use default profile (complete)
inkcollector lorcast get-cards --set-id set_123

# Override to use images-only profile
inkcollector --profile images-only lorcast get-cards --set-id set_123

# Override to use preview profile
inkcollector --profile preview lorcast get-cards --set-id set_123
```

## Configuration File Location

Inkcollector searches for `.inkcollector.yaml` in:

1. Current working directory
2. Parent directory
3. Parent's parent directory
4. Parent's parent's parent directory

If no configuration file is found, default settings are used.

You can also specify a configuration file explicitly:

```bash
inkcollector --config /path/to/config.yaml command
```

## Migration from CLI-only Usage

If you're migrating from using only command line options, you can create equivalent configurations:

### Before (CLI only)
```bash
inkcollector lorcast get-cards --set-id set_123 --save-json --get-images normal
```

### After (with configuration)
Create a profile in `.inkcollector.yaml`:
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

Then use:
```bash
inkcollector --profile my-profile lorcast get-cards --set-id set_123
```

## Troubleshooting

### Configuration Not Loading

If your configuration isn't loading:

1. Check file name: must be `.inkcollector.yaml`
2. Check YAML syntax: use `inkcollector config show` to validate
3. Check file location: must be in current directory or parent directories
4. Use `--config` to specify exact path

### Invalid Configuration

If you get YAML errors:

1. Validate YAML syntax online or with a YAML linter
2. Check indentation (use spaces, not tabs)
3. Ensure all required fields are present
4. Use `inkcollector config init` to create a valid template

### Profile Not Found

If you get "profile not found" warnings:

1. Check profile name spelling in configuration
2. Use `inkcollector config list --profiles` to see available profiles
3. Verify the configuration file is being loaded correctly
