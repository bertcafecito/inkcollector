.. _examples:

========
Examples
========

Real-world usage examples and workflows for common Inkcollector scenarios.

Quick Start Examples
===================

Basic Data Collection
---------------------

Collect all sets and explore available data:

.. code-block:: shell

    # Get all sets (saves to data/lorcast/sets.json)
    inkcollector lorcast get-sets
    
    # Preview sets in console to see available set IDs
    inkcollector --profile preview lorcast get-sets
    
    # Get cards from "The First Chapter" set
    inkcollector lorcast get-cards --set-id TFC

Complete Set Collection
----------------------

Download everything for a specific set:

.. code-block:: shell

    # Get data and images for TFC set
    inkcollector lorcast get-cards --set-id TFC --get-images
    
    # Get high-quality images
    inkcollector lorcast get-cards --set-id TFC --get-images large
    
    # Get multiple sets
    inkcollector lorcast get-cards --set-id TFC --get-images
    inkcollector lorcast get-cards --set-id ROF --get-images
    inkcollector lorcast get-cards --set-id ITI --get-images

Configuration-Based Workflows
=============================

Setting Up for Research
-----------------------

Create a research-focused configuration:

**`.inkcollector.yaml`**:

.. code-block:: yaml

    default_workspace: research

    profiles:
      research-complete:
        description: "Complete data with high-quality images"
        extract_data: true
        extract_images: true
        image_size: large
        save_json: true
        print_json: true  # Show data for verification

      research-preview:
        description: "Quick data preview"
        extract_data: true
        extract_images: false
        save_json: false
        print_json: true

    workspaces:
      research:
        data_output_dir: research/lorcana-data
        image_output_dir: research/lorcana-images
        default_profile: research-complete

**Usage:**

.. code-block:: shell

    # Quick exploration
    inkcollector --profile research-preview lorcast get-sets
    
    # Complete data collection
    inkcollector lorcast get-cards --set-id TFC --get-images
    inkcollector lorcast get-cards --set-id ROF --get-images

**Result structure:**

.. code-block:: text

    research/
    ├── lorcana-data/
    │   └── lorcast/
    │       ├── sets.json
    │       └── sets/
    │           ├── TFC.json
    │           └── ROF.json
    └── lorcana-images/
        └── lorcast/
            └── sets/
                ├── TFC/
                │   └── [204 card images]
                └── ROF/
                    └── [204 card images]

Website Asset Generation
-----------------------

Generate optimized assets for a website:

**`.inkcollector.yaml`**:

.. code-block:: yaml

    default_workspace: website

    profiles:
      web-thumbnails:
        description: "Small images for thumbnails"
        extract_data: false
        extract_images: true
        image_size: small
        save_json: false
        print_json: false

      web-data:
        description: "JSON data for API"
        extract_data: true
        extract_images: false
        save_json: true
        print_json: false

    workspaces:
      website:
        data_output_dir: website/api/data
        image_output_dir: website/public/images
        default_profile: web-thumbnails

**Usage:**

.. code-block:: shell

    # Generate API data
    inkcollector --profile web-data lorcast get-sets
    inkcollector --profile web-data lorcast get-cards --set-id TFC
    
    # Generate thumbnail images
    inkcollector --profile web-thumbnails lorcast get-cards --set-id TFC --get-images

**Result structure:**

.. code-block:: text

    website/
    ├── api/
    │   └── data/
    │       └── lorcast/
    │           ├── sets.json
    │           └── sets/
    │               └── TFC.json
    └── public/
        └── images/
            └── lorcast/
                └── sets/
                    └── TFC/
                        └── [204 small images]

Development Workflow Examples
============================

Multi-Environment Setup
-----------------------

Set up development, staging, and production environments:

**`dev-config.yaml`**:

.. code-block:: yaml

    default_workspace: dev
    
    profiles:
      dev-quick:
        description: "Quick testing"
        extract_data: true
        extract_images: false
        save_json: false
        print_json: true
    
    workspaces:
      dev:
        data_output_dir: tmp/dev-data
        image_output_dir: tmp/dev-images
        default_profile: dev-quick

**`prod-config.yaml`**:

.. code-block:: yaml

    default_workspace: production
    
    profiles:
      prod-archive:
        description: "Production archival"
        extract_data: true
        extract_images: true
        image_size: large
        save_json: true
        print_json: false
    
    workspaces:
      production:
        data_output_dir: data/lorcana
        image_output_dir: assets/lorcana
        default_profile: prod-archive

**Usage:**

.. code-block:: shell

    # Development testing
    inkcollector --config dev-config.yaml lorcast get-sets
    inkcollector --config dev-config.yaml lorcast get-cards --set-id TFC
    
    # Production deployment
    inkcollector --config prod-config.yaml lorcast get-sets
    inkcollector --config prod-config.yaml lorcast get-cards --set-id TFC --get-images

Team Collaboration
------------------

Shared configuration for team projects:

**`team-config.yaml`**:

.. code-block:: yaml

    default_workspace: shared

    profiles:
      team-standard:
        description: "Standard team data collection"
        extract_data: true
        extract_images: true
        image_size: normal
        save_json: true
        print_json: false

      team-preview:
        description: "Team data preview"
        extract_data: true
        extract_images: false
        save_json: false
        print_json: true

    workspaces:
      shared:
        data_output_dir: team/shared/data
        image_output_dir: team/shared/images
        default_profile: team-standard

      personal:
        data_output_dir: team/personal/{{ USER }}/data
        image_output_dir: team/personal/{{ USER }}/images
        default_profile: team-standard

**Usage:**

.. code-block:: shell

    # Team member Alice
    inkcollector --config team-config.yaml --workspace shared lorcast get-sets
    
    # Personal workspace
    inkcollector --config team-config.yaml --workspace personal lorcast get-cards --set-id TFC --get-images

Advanced Use Cases
=================

Data Analysis Pipeline
---------------------

Extract data for analysis without images:

.. code-block:: shell

    # Set up analysis workspace
    inkcollector config init

Edit configuration for analysis:

.. code-block:: yaml

    default_workspace: analysis

    profiles:
      analysis-data:
        description: "Data-only extraction for analysis"
        extract_data: true
        extract_images: false
        save_json: true
        print_json: true  # Show data for verification

    workspaces:
      analysis:
        data_output_dir: analysis/raw-data
        image_output_dir: analysis/images  # unused
        default_profile: analysis-data

**Collection workflow:**

.. code-block:: shell

    # Collect all sets data
    inkcollector lorcast get-sets
    
    # Collect all available sets (get set IDs first)
    inkcollector --profile preview lorcast get-sets | grep '"id"'
    
    # Collect each set's cards
    inkcollector lorcast get-cards --set-id TFC
    inkcollector lorcast get-cards --set-id ROF  
    inkcollector lorcast get-cards --set-id ITI

Image Archive Creation
---------------------

Create a complete image archive:

.. code-block:: yaml

    default_workspace: archive

    profiles:
      archive-complete:
        description: "Complete archival with all image sizes"
        extract_data: true
        extract_images: true
        image_size: large
        save_json: true
        print_json: false

    workspaces:
      archive:
        data_output_dir: archive/lorcana/data
        image_output_dir: archive/lorcana/images
        default_profile: archive-complete

**Archive workflow:**

.. code-block:: shell

    # Create complete archive
    inkcollector lorcast get-sets
    
    # Archive each set with large images
    for set_id in TFC ROF ITI URR SSK; do
        echo "Archiving set: $set_id"
        inkcollector lorcast get-cards --set-id $set_id --get-images
    done

Content Creation Workflow
-------------------------

Generate content for blogs, articles, or presentations:

.. code-block:: yaml

    default_workspace: content

    profiles:
      content-preview:
        description: "Preview content for articles"
        extract_data: true
        extract_images: false
        save_json: false
        print_json: true

      content-images:
        description: "High-quality images for content"
        extract_data: false
        extract_images: true
        image_size: large
        save_json: false
        print_json: false

    workspaces:
      content:
        data_output_dir: content/data
        image_output_dir: content/images
        default_profile: content-preview

**Content creation workflow:**

.. code-block:: shell

    # Explore data for article ideas
    inkcollector --profile content-preview lorcast get-sets
    inkcollector --profile content-preview lorcast get-cards --set-id TFC
    
    # Download specific images for articles
    inkcollector --profile content-images lorcast get-cards --set-id TFC --get-images

Custom Directory Control
========================

Override Default Paths
----------------------

Take complete control over where files are saved, bypassing the default ``lorcast/`` subdirectory structure:

.. code-block:: shell

    # Default behavior: structured subdirectories
    inkcollector lorcast get-sets --save-json
    # → Saves to: data/lorcast/sets.json
    
    inkcollector lorcast get-cards --set-id TFC --save-json --get-images
    # → Data: data/lorcast/sets/TFC.json
    # → Images: images/lorcast/sets/TFC/crd_*.jpg
    
    # Custom directories: full override
    inkcollector --output-dir /project/data lorcast get-sets --save-json
    # → Saves to: /project/data/sets.json
    
    inkcollector --output-dir /project/cards --image-dir /project/images lorcast get-cards --set-id TFC --save-json --get-images
    # → Data: /project/cards/TFC.json
    # → Images: /project/images/crd_*.jpg

Cross-Platform Paths
--------------------

Custom directories work across operating systems:

.. code-block:: shell

    # Windows
    inkcollector --output-dir "C:\MyProject\Data" --image-dir "C:\MyProject\Images" lorcast get-cards --set-id TFC --save-json --get-images
    
    # macOS/Linux
    inkcollector --output-dir "/Users/username/project/data" --image-dir "/Users/username/project/images" lorcast get-cards --set-id TFC --save-json --get-images
    
    # Relative paths (from current directory)
    inkcollector --output-dir "./project-data" --image-dir "./project-images" lorcast get-cards --set-id TFC --save-json --get-images

Project Organization
-------------------

Organize different projects with custom directories:

.. code-block:: shell

    # Research project
    inkcollector --output-dir /research/lorcana/data --image-dir /research/lorcana/images lorcast get-sets --save-json
    inkcollector --output-dir /research/lorcana/data --image-dir /research/lorcana/images lorcast get-cards --set-id TFC --save-json --get-images
    
    # Website project (different organization)
    inkcollector --output-dir /website/api/data --image-dir /website/static/cards lorcast get-sets --save-json
    inkcollector --output-dir /website/api/data --image-dir /website/static/cards lorcast get-cards --set-id TFC --save-json --get-images
    
    # Backup/archive (timestamp-based)
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    inkcollector --output-dir "/backup/lorcana_$TIMESTAMP/data" --image-dir "/backup/lorcana_$TIMESTAMP/images" lorcast get-sets --save-json

Mixed Configurations
-------------------

Combine custom directories with other features:

.. code-block:: shell

    # Custom directories with profiles
    inkcollector --output-dir /backup/data --profile complete lorcast get-cards --set-id TFC
    
    # Custom directories with workspaces (directories override workspace settings)
    inkcollector --workspace research --output-dir /external/drive/data lorcast get-sets --save-json
    
    # Custom directories with config files
    inkcollector --config project.yaml --output-dir /project/override/data lorcast get-cards --set-id TFC --save-json
    
    # Only override one directory
    inkcollector --output-dir /custom/data lorcast get-cards --set-id TFC --save-json --get-images
    # → Data: /custom/data/TFC.json
    # → Images: {workspace.image_output_dir}/lorcast/sets/TFC/crd_*.jpg

File Organization Comparison
---------------------------

**Default structure (workspace-based):**

.. code-block:: text

    workspace-dir/
    ├── data/
    │   └── lorcast/
    │       ├── sets.json
    │       └── sets/
    │           ├── TFC.json
    │           └── ROF.json
    └── images/
        └── lorcast/
            └── sets/
                ├── TFC/
                │   └── [card images]
                └── ROF/
                    └── [card images]

**Custom directory structure (full override):**

.. code-block:: text

    /project/
    ├── data/
    │   ├── sets.json         # Direct placement
    │   ├── TFC.json          # Direct placement
    │   └── ROF.json          # Direct placement
    └── images/
        └── [all card images] # Direct placement, no subdirectories

Integration Examples
===================

GitHub Actions Workflow
-----------------------

Automate data collection with GitHub Actions:

**`.github/workflows/collect-data.yml`**:

.. code-block:: yaml

    name: Collect Lorcana Data
    
    on:
      schedule:
        - cron: '0 6 * * *'  # Daily at 6 AM
      workflow_dispatch:
    
    jobs:
      collect:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v3
          
          - name: Set up Python
            uses: actions/setup-python@v4
            with:
              python-version: '3.11'
              
          - name: Install Inkcollector
            run: pip install inkcollector
            
          - name: Collect data
            run: |
              inkcollector config init
              inkcollector lorcast get-sets
              inkcollector lorcast get-cards --set-id TFC
              
          - name: Commit results
            run: |
              git config --local user.email "action@github.com"
              git config --local user.name "GitHub Action"
              git add data/
              git commit -m "Update Lorcana data" || exit 0
              git push

Docker Integration
-----------------

Use Inkcollector in Docker containers:

**`Dockerfile`**:

.. code-block:: dockerfile

    FROM python:3.11-slim
    
    WORKDIR /app
    
    RUN pip install inkcollector
    
    COPY .inkcollector.yaml .
    
    CMD ["inkcollector", "lorcast", "get-sets"]

**`docker-compose.yml`**:

.. code-block:: yaml

    version: '3.8'
    
    services:
      data-collector:
        build: .
        volumes:
          - ./data:/app/data
          - ./images:/app/images
        environment:
          - INKCOLLECTOR_WORKSPACE=production

**Usage:**

.. code-block:: shell

    # Build and run
    docker-compose up data-collector
    
    # Run specific commands
    docker-compose run data-collector inkcollector lorcast get-cards --set-id TFC --get-images

Scripting Examples
=================

Bash Automation
---------------

Automate collection across multiple sets:

**`collect-all-sets.sh`**:

.. code-block:: bash

    #!/bin/bash
    
    # Get all sets first
    echo "Fetching all sets..."
    inkcollector lorcast get-sets
    
    # Extract set IDs from the JSON
    SET_IDS=$(inkcollector --profile preview lorcast get-sets | grep '"id":' | sed 's/.*"id": "\([^"]*\)".*/\1/')
    
    echo "Found sets: $SET_IDS"
    
    # Collect each set
    for set_id in $SET_IDS; do
        echo "Collecting set: $set_id"
        inkcollector lorcast get-cards --set-id "$set_id" --get-images
        
        # Add delay to be nice to the API
        sleep 2
    done
    
    echo "Collection complete!"

**Usage:**

.. code-block:: shell

    chmod +x collect-all-sets.sh
    ./collect-all-sets.sh

Python Integration
-----------------

Use Inkcollector output in Python scripts:

**`analyze-data.py`**:

.. code-block:: python

    #!/usr/bin/env python3
    
    import json
    import subprocess
    import sys
    from pathlib import Path
    
    def collect_set_data(set_id):
        """Collect data for a set using Inkcollector."""
        cmd = [
            'inkcollector', 
            '--profile', 'data-only',
            'lorcast', 'get-cards',
            '--set-id', set_id
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error collecting {set_id}: {result.stderr}")
            return None
            
        # Load the saved JSON
        data_file = Path(f"data/lorcast/sets/{set_id}.json")
        if data_file.exists():
            with open(data_file) as f:
                return json.load(f)
        return None
    
    def analyze_set(set_id):
        """Analyze a set's data."""
        data = collect_set_data(set_id)
        if not data:
            return
            
        cards = data.get('results', [])
        print(f"\nSet {set_id} Analysis:")
        print(f"  Total cards: {len(cards)}")
        
        # Analyze by rarity
        rarities = {}
        for card in cards:
            rarity = card.get('rarity', 'Unknown')
            rarities[rarity] = rarities.get(rarity, 0) + 1
            
        print("  By rarity:")
        for rarity, count in sorted(rarities.items()):
            print(f"    {rarity}: {count}")
    
    if __name__ == "__main__":
        sets_to_analyze = sys.argv[1:] if len(sys.argv) > 1 else ['TFC', 'ROF']
        
        for set_id in sets_to_analyze:
            analyze_set(set_id)

**Usage:**

.. code-block:: shell

    python analyze-data.py TFC ROF ITI

Troubleshooting Examples
=======================

Common Issue Solutions
---------------------

**Problem:** Permission denied creating directories

.. code-block:: shell

    # Solution: Use a different workspace
    inkcollector --workspace temp lorcast get-sets

**Configuration:** 

.. code-block:: yaml

    workspaces:
      temp:
        data_output_dir: /tmp/lorcana-data
        image_output_dir: /tmp/lorcana-images
        default_profile: complete

**Problem:** API timeouts or network issues

.. code-block:: shell

    # Solution: Use preview profile to test connectivity
    inkcollector --profile preview lorcast get-sets
    
    # If that works, try data-only first
    inkcollector --profile data-only lorcast get-cards --set-id TFC
    
    # Then add images separately
    inkcollector --profile images-only lorcast get-cards --set-id TFC --get-images

**Problem:** Disk space issues

.. code-block:: shell

    # Solution: Use small images and selective collection
    inkcollector --profile images-only lorcast get-cards --set-id TFC --get-images small
    
    # Or data-only for analysis
    inkcollector --profile data-only lorcast get-cards --set-id TFC

Performance Examples
===================

Optimized Collection
-------------------

For large-scale collection, optimize the workflow:

.. code-block:: shell

    # 1. Get metadata first (fast)
    inkcollector --profile data-only lorcast get-sets
    inkcollector --profile data-only lorcast get-cards --set-id TFC
    inkcollector --profile data-only lorcast get-cards --set-id ROF
    
    # 2. Download images separately (can be interrupted/resumed)
    inkcollector --profile images-only lorcast get-cards --set-id TFC --get-images small
    inkcollector --profile images-only lorcast get-cards --set-id ROF --get-images small

Selective Collection
-------------------

Collect only what you need:

.. code-block:: shell

    # Explore first
    inkcollector --profile preview lorcast get-sets
    
    # Get only recent sets
    inkcollector lorcast get-cards --set-id SSK --get-images  # Newest set
    
    # Get only specific image sizes
    inkcollector --profile images-only lorcast get-cards --set-id TFC --get-images small  # Thumbnails
    inkcollector --profile images-only lorcast get-cards --set-id TFC --get-images large  # High-res

Next Steps
==========

- Check out :doc:`troubleshooting` for solutions to common issues
- Read :doc:`cli-reference` for complete command documentation
- Learn more about :doc:`configuration` and :doc:`profiles-workspaces`
