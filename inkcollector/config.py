"""Configuration management for Inkcollector.

This module provides configuration file support for the Inkcollector application,
allowing users to define default settings, extraction profiles, and workspace
configurations using YAML files.
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, field


@dataclass
class ExtractionProfile:
    """Defines what data and files to extract."""
    name: str
    description: str = ""
    extract_data: bool = True
    extract_images: bool = True
    image_size: str = "normal"  # small, normal, large
    save_json: bool = True
    print_json: bool = False


@dataclass
class WorkspaceConfig:
    """Workspace-specific configuration."""
    name: str = "default"
    data_output_dir: str = "data"
    image_output_dir: str = "images"
    default_profile: str = "complete"


@dataclass
class InkcollectorConfig:
    """Main configuration class for Inkcollector."""
    # Default settings
    default_workspace: str = "default"
    
    # API configuration
    api_base_url: str = "https://api.lorcast.com"
    api_version: str = "v0"
    
    # Extraction profiles
    profiles: Dict[str, ExtractionProfile] = field(default_factory=dict)
    
    # Workspace configurations
    workspaces: Dict[str, WorkspaceConfig] = field(default_factory=dict)
    
    def __post_init__(self):
        """Initialize default profiles and workspaces if not provided."""
        if not self.profiles:
            self._create_default_profiles()
        if not self.workspaces:
            self._create_default_workspace()
    
    def _create_default_profiles(self):
        """Create default extraction profiles."""
        self.profiles = {
            "complete": ExtractionProfile(
                name="complete",
                description="Extract all data and images",
                extract_data=True,
                extract_images=True,
                image_size="normal",
                save_json=True,
                print_json=False
            ),
            "images-only": ExtractionProfile(
                name="images-only",
                description="Extract only card images",
                extract_data=False,
                extract_images=True,
                image_size="normal",
                save_json=False,
                print_json=False
            ),
            "data-only": ExtractionProfile(
                name="data-only",
                description="Extract only JSON data",
                extract_data=True,
                extract_images=False,
                image_size="normal",
                save_json=True,
                print_json=False
            ),
            "preview": ExtractionProfile(
                name="preview",
                description="Show data in console without saving",
                extract_data=True,
                extract_images=False,
                image_size="normal",
                save_json=False,
                print_json=True
            )
        }
    
    def _create_default_workspace(self):
        """Create default workspace configuration."""
        self.workspaces = {
            "default": WorkspaceConfig(
                name="default",
                data_output_dir="data",
                image_output_dir="images",
                default_profile="complete"
            )
        }
    
    def get_profile(self, profile_name: str) -> Optional[ExtractionProfile]:
        """Get an extraction profile by name."""
        return self.profiles.get(profile_name)
    
    def get_workspace(self, workspace_name: str) -> Optional[WorkspaceConfig]:
        """Get a workspace configuration by name."""
        return self.workspaces.get(workspace_name)
    
    def list_profiles(self) -> List[str]:
        """Get list of available profile names."""
        return list(self.profiles.keys())
    
    def list_workspaces(self) -> List[str]:
        """Get list of available workspace names."""
        return list(self.workspaces.keys())


class ConfigManager:
    """Manages loading and saving configuration files."""
    
    CONFIG_FILENAME = ".inkcollector.yaml"
    
    def __init__(self):
        """Initialize the config manager."""
        self._config: Optional[InkcollectorConfig] = None
    
    def load_config(self, config_path: Optional[str] = None) -> InkcollectorConfig:
        """Load configuration from file or create default.
        
        Args:
            config_path: Optional path to config file. If None, searches for
                        .inkcollector.yaml in current directory and parent directories.
        
        Returns:
            InkcollectorConfig instance
        """
        if config_path:
            config_file = Path(config_path)
        else:
            config_file = self._find_config_file()
        
        if config_file and config_file.exists():
            self._config = self._load_from_file(config_file)
        else:
            self._config = InkcollectorConfig()
        
        return self._config
    
    def _find_config_file(self) -> Optional[Path]:
        """Find config file by searching current directory and parents."""
        current_dir = Path.cwd()
        
        # Search in current directory and up to 3 parent directories
        for _ in range(4):
            config_file = current_dir / self.CONFIG_FILENAME
            if config_file.exists():
                return config_file
            
            parent = current_dir.parent
            if parent == current_dir:  # Reached root
                break
            current_dir = parent
        
        return None
    
    def _load_from_file(self, config_file: Path) -> InkcollectorConfig:
        """Load configuration from YAML file."""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            
            return self._parse_config_data(data)
        
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in config file {config_file}: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"Config file not found: {config_file}")
        except Exception as e:
            raise ValueError(f"Error loading config file {config_file}: {e}")
    
    def _parse_config_data(self, data: Dict[str, Any]) -> InkcollectorConfig:
        """Parse configuration data from dictionary."""
        # Parse profiles
        profiles = {}
        if 'profiles' in data:
            for name, profile_data in data['profiles'].items():
                profiles[name] = ExtractionProfile(
                    name=name,
                    description=profile_data.get('description', ''),
                    extract_data=profile_data.get('extract_data', True),
                    extract_images=profile_data.get('extract_images', True),
                    image_size=profile_data.get('image_size', 'normal'),
                    save_json=profile_data.get('save_json', True),
                    print_json=profile_data.get('print_json', False)
                )
        
        # Parse workspaces
        workspaces = {}
        if 'workspaces' in data:
            for name, workspace_data in data['workspaces'].items():
                workspaces[name] = WorkspaceConfig(
                    name=name,
                    data_output_dir=workspace_data.get('data_output_dir', 'data'),
                    image_output_dir=workspace_data.get('image_output_dir', 'images'),
                    default_profile=workspace_data.get('default_profile', 'complete')
                )
        
        # Create main config
        config = InkcollectorConfig(
            default_workspace=data.get('default_workspace', 'default'),
            api_base_url=data.get('api_base_url', 'https://api.lorcast.com'),
            api_version=data.get('api_version', 'v0'),
            profiles=profiles,
            workspaces=workspaces
        )
        
        return config
    
    def save_config(self, config: InkcollectorConfig, config_path: str) -> None:
        """Save configuration to YAML file.
        
        Args:
            config: Configuration to save
            config_path: Path where to save the config file
        """
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert config to dictionary
        data = self._config_to_dict(config)
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False, indent=2)
        except Exception as e:
            raise ValueError(f"Error saving config to {config_file}: {e}")
    
    def _config_to_dict(self, config: InkcollectorConfig) -> Dict[str, Any]:
        """Convert configuration object to dictionary for YAML serialization."""
        data = {
            'default_workspace': config.default_workspace,
            'api_base_url': config.api_base_url,
            'api_version': config.api_version,
        }
        
        # Convert profiles
        if config.profiles:
            data['profiles'] = {}
            for name, profile in config.profiles.items():
                data['profiles'][name] = {
                    'description': profile.description,
                    'extract_data': profile.extract_data,
                    'extract_images': profile.extract_images,
                    'image_size': profile.image_size,
                    'save_json': profile.save_json,
                    'print_json': profile.print_json
                }
        
        # Convert workspaces
        if config.workspaces:
            data['workspaces'] = {}
            for name, workspace in config.workspaces.items():
                data['workspaces'][name] = {
                    'data_output_dir': workspace.data_output_dir,
                    'image_output_dir': workspace.image_output_dir,
                    'default_profile': workspace.default_profile
                }
        
        return data
    
    def create_sample_config(self, config_path: str) -> None:
        """Create a sample configuration file with all default options.
        
        Args:
            config_path: Path where to create the sample config file
        """
        config = InkcollectorConfig()
        self.save_config(config, config_path)
    
    @property
    def config(self) -> Optional[InkcollectorConfig]:
        """Get the currently loaded configuration."""
        return self._config
