"""Tests for the configuration system."""

import pytest
import tempfile
import os
from pathlib import Path
import yaml

from inkcollector.config import ConfigManager, InkcollectorConfig, ExtractionProfile, WorkspaceConfig


class TestExtractionProfile:
    """Test ExtractionProfile dataclass."""

    def test_default_profile(self):
        """Test creating a profile with default values."""
        profile = ExtractionProfile(name="test")
        assert profile.name == "test"
        assert profile.description == ""
        assert profile.extract_data is True
        assert profile.extract_images is True
        assert profile.image_size == "normal"
        assert profile.save_json is True
        assert profile.print_json is False

    def test_custom_profile(self):
        """Test creating a profile with custom values."""
        profile = ExtractionProfile(
            name="custom",
            description="Custom profile",
            extract_data=False,
            extract_images=True,
            image_size="large",
            save_json=False,
            print_json=True
        )
        assert profile.name == "custom"
        assert profile.description == "Custom profile"
        assert profile.extract_data is False
        assert profile.extract_images is True
        assert profile.image_size == "large"
        assert profile.save_json is False
        assert profile.print_json is True


class TestWorkspaceConfig:
    """Test WorkspaceConfig dataclass."""

    def test_default_workspace(self):
        """Test creating a workspace with default values."""
        workspace = WorkspaceConfig()
        assert workspace.name == "default"
        assert workspace.data_output_dir == "data"
        assert workspace.image_output_dir == "images"
        assert workspace.default_profile == "complete"

    def test_custom_workspace(self):
        """Test creating a workspace with custom values."""
        workspace = WorkspaceConfig(
            name="research",
            data_output_dir="research/data",
            image_output_dir="research/images",
            default_profile="data-only"
        )
        assert workspace.name == "research"
        assert workspace.data_output_dir == "research/data"
        assert workspace.image_output_dir == "research/images"
        assert workspace.default_profile == "data-only"


class TestInkcollectorConfig:
    """Test InkcollectorConfig dataclass."""

    def test_default_config(self):
        """Test creating config with default values."""
        config = InkcollectorConfig()
        assert config.default_workspace == "default"
        assert config.api_base_url == "https://api.lorcast.com"
        assert config.api_version == "v0"
        assert len(config.profiles) == 4  # complete, images-only, data-only, preview
        assert len(config.workspaces) == 1  # default

    def test_get_profile(self):
        """Test getting profiles by name."""
        config = InkcollectorConfig()
        
        complete_profile = config.get_profile("complete")
        assert complete_profile is not None
        assert complete_profile.name == "complete"
        assert complete_profile.extract_data is True
        assert complete_profile.extract_images is True

        images_only_profile = config.get_profile("images-only")
        assert images_only_profile is not None
        assert images_only_profile.name == "images-only"
        assert images_only_profile.extract_data is False
        assert images_only_profile.extract_images is True

        nonexistent_profile = config.get_profile("nonexistent")
        assert nonexistent_profile is None

    def test_get_workspace(self):
        """Test getting workspaces by name."""
        config = InkcollectorConfig()
        
        default_workspace = config.get_workspace("default")
        assert default_workspace is not None
        assert default_workspace.name == "default"

        nonexistent_workspace = config.get_workspace("nonexistent")
        assert nonexistent_workspace is None

    def test_list_profiles(self):
        """Test listing profile names."""
        config = InkcollectorConfig()
        profiles = config.list_profiles()
        assert "complete" in profiles
        assert "images-only" in profiles
        assert "data-only" in profiles
        assert "preview" in profiles
        assert len(profiles) == 4

    def test_list_workspaces(self):
        """Test listing workspace names."""
        config = InkcollectorConfig()
        workspaces = config.list_workspaces()
        assert "default" in workspaces
        assert len(workspaces) == 1


class TestConfigManager:
    """Test ConfigManager class."""

    def test_load_default_config(self):
        """Test loading default config when no file exists."""
        # Simply test that default config loads correctly
        manager = ConfigManager()
        # Pass a non-existent path to force default config
        config = manager.load_config("/nonexistent/path/config.yaml")
        
        assert isinstance(config, InkcollectorConfig)
        assert config.default_workspace == "default"
        assert len(config.profiles) == 4
        assert len(config.workspaces) == 1

    def test_load_config_from_file(self):
        """Test loading config from YAML file."""
        config_data = {
            'default_workspace': 'test',
            'api_base_url': 'https://test.api.com',
            'api_version': 'v1',
            'profiles': {
                'test-profile': {
                    'description': 'Test profile',
                    'extract_data': True,
                    'extract_images': False,
                    'image_size': 'small',
                    'save_json': True,
                    'print_json': False
                }
            },
            'workspaces': {
                'test-workspace': {
                    'data_output_dir': 'test/data',
                    'image_output_dir': 'test/images',
                    'default_profile': 'test-profile'
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config_data, f)
            config_file = f.name
        
        try:
            manager = ConfigManager()
            config = manager.load_config(config_file)
            
            assert config.default_workspace == 'test'
            assert config.api_base_url == 'https://test.api.com'
            assert config.api_version == 'v1'
            
            profile = config.get_profile('test-profile')
            assert profile is not None
            assert profile.description == 'Test profile'
            assert profile.extract_data is True
            assert profile.extract_images is False
            assert profile.image_size == 'small'
            
            workspace = config.get_workspace('test-workspace')
            assert workspace is not None
            assert workspace.data_output_dir == 'test/data'
            assert workspace.image_output_dir == 'test/images'
            assert workspace.default_profile == 'test-profile'
            
        finally:
            os.unlink(config_file)

    def test_save_config(self):
        """Test saving config to YAML file."""
        config = InkcollectorConfig()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_file = f.name
        
        try:
            manager = ConfigManager()
            manager.save_config(config, config_file)
            
            # Load the saved file and verify it
            with open(config_file, 'r') as f:
                saved_data = yaml.safe_load(f)
            
            assert saved_data['default_workspace'] == 'default'
            assert saved_data['api_base_url'] == 'https://api.lorcast.com'
            assert saved_data['api_version'] == 'v0'
            assert 'profiles' in saved_data
            assert 'workspaces' in saved_data
            
        finally:
            os.unlink(config_file)

    def test_create_sample_config(self):
        """Test creating a sample config file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_file = f.name
        
        try:
            manager = ConfigManager()
            manager.create_sample_config(config_file)
            
            # Verify the file was created and contains expected content
            assert os.path.exists(config_file)
            
            with open(config_file, 'r') as f:
                saved_data = yaml.safe_load(f)
            
            assert saved_data['default_workspace'] == 'default'
            assert 'profiles' in saved_data
            assert 'workspaces' in saved_data
            
        finally:
            os.unlink(config_file)

    def test_find_config_file(self):
        """Test finding config file in parent directories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create nested directory structure
            nested_dir = os.path.join(temp_dir, 'nested', 'deep')
            os.makedirs(nested_dir)
            
            # Create config file in parent directory
            config_file = os.path.join(temp_dir, '.inkcollector.yaml')
            with open(config_file, 'w') as f:
                yaml.dump({'test': 'data'}, f)
            
            # Change to nested directory
            original_cwd = os.getcwd()
            try:
                os.chdir(nested_dir)
                
                manager = ConfigManager()
                found_file = manager._find_config_file()
                
                assert found_file is not None
                assert found_file.name == '.inkcollector.yaml'
                assert found_file.exists()
                
            finally:
                os.chdir(original_cwd)

    def test_invalid_yaml_file(self):
        """Test handling of invalid YAML file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("invalid: yaml: content: [")
            config_file = f.name
        
        try:
            manager = ConfigManager()
            with pytest.raises(ValueError, match="Invalid YAML"):
                manager.load_config(config_file)
                
        finally:
            os.unlink(config_file)
