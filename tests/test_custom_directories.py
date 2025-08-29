"""
Test suite for custom output directory functionality.

This module contains comprehensive tests for the custom --output-dir and --image-dir
flags, including directory override logic, file placement behavior, and interaction
with existing configuration.
"""

import argparse
import os
import tempfile
from unittest.mock import Mock, call, mock_open, patch

import pytest

from inkcollector.cli import InkcollectorCLI
from inkcollector.lorcast import LorcastAPI


class TestCustomDirectories:
    """Test class for custom directory functionality."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir

    @pytest.fixture
    def cli(self, temp_dir):
        """Create a CLI instance with temporary directories."""
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            cli = InkcollectorCLI()
            cli.data_output_dir = os.path.join(temp_dir, "data")
            cli.image_output_dir = os.path.join(temp_dir, "images")
            cli.using_custom_data_dir = False
            cli.using_custom_image_dir = False
            return cli

    @pytest.fixture
    def mock_lorcast_api(self):
        """Create a mock LorcastAPI instance."""
        return Mock(spec=LorcastAPI)

    def test_parser_has_output_dir_arguments(self, cli):
        """Test that the parser includes --output-dir and --image-dir arguments."""
        # Test get-sets command has the flags
        args = cli.parser.parse_args([
            "lorcast", "get-sets", 
            "--output-dir", "/custom/data",
            "--image-dir", "/custom/images"
        ])
        assert args.output_dir == "/custom/data"
        assert args.image_dir == "/custom/images"

        # Test get-cards command has the flags
        args = cli.parser.parse_args([
            "lorcast", "get-cards", 
            "--set-id", "test-set",
            "--output-dir", "/custom/data",
            "--image-dir", "/custom/images"
        ])
        assert args.output_dir == "/custom/data"
        assert args.image_dir == "/custom/images"

    def test_apply_directory_overrides_with_custom_data_dir(self, cli):
        """Test applying custom data directory override."""
        custom_dir = os.path.abspath("/custom/data")
        args = argparse.Namespace(output_dir=custom_dir, image_dir=None)
        
        with (
            patch.object(cli, "_create_directory_if_not_exists") as mock_create_dir,
            patch("builtins.print") as mock_print,
        ):
            cli._apply_directory_overrides(args)

        assert cli.data_output_dir == custom_dir
        assert cli.using_custom_data_dir is True
        assert cli.using_custom_image_dir is False
        mock_create_dir.assert_called_once_with(custom_dir)
        mock_print.assert_called_once_with(
            f"Using custom data output directory: {custom_dir}"
        )

    def test_apply_directory_overrides_with_custom_image_dir(self, cli):
        """Test applying custom image directory override."""
        custom_dir = os.path.abspath("/custom/images")
        args = argparse.Namespace(output_dir=None, image_dir=custom_dir)
        
        with (
            patch.object(cli, "_create_directory_if_not_exists") as mock_create_dir,
            patch("builtins.print") as mock_print,
        ):
            cli._apply_directory_overrides(args)

        assert cli.image_output_dir == custom_dir
        assert cli.using_custom_data_dir is False
        assert cli.using_custom_image_dir is True
        mock_create_dir.assert_called_once_with(custom_dir)
        mock_print.assert_called_once_with(
            f"Using custom image output directory: {custom_dir}"
        )

    def test_apply_directory_overrides_with_both_custom_dirs(self, cli):
        """Test applying both custom directory overrides."""
        custom_data_dir = os.path.abspath("/custom/data")
        custom_image_dir = os.path.abspath("/custom/images")
        args = argparse.Namespace(
            output_dir=custom_data_dir, 
            image_dir=custom_image_dir
        )
        
        with (
            patch.object(cli, "_create_directory_if_not_exists") as mock_create_dir,
            patch("builtins.print") as mock_print,
        ):
            cli._apply_directory_overrides(args)

        assert cli.data_output_dir == custom_data_dir
        assert cli.image_output_dir == custom_image_dir
        assert cli.using_custom_data_dir is True
        assert cli.using_custom_image_dir is True
        
        # Check that both directories were created
        expected_calls = [call(custom_data_dir), call(custom_image_dir)]
        mock_create_dir.assert_has_calls(expected_calls)
        
        # Check both print messages
        expected_print_calls = [
            call(f"Using custom data output directory: {custom_data_dir}"),
            call(f"Using custom image output directory: {custom_image_dir}")
        ]
        mock_print.assert_has_calls(expected_print_calls)

    def test_apply_directory_overrides_no_custom_dirs(self, cli):
        """Test that no overrides are applied when no custom directories specified."""
        original_data_dir = cli.data_output_dir
        original_image_dir = cli.image_output_dir
        
        args = argparse.Namespace(output_dir=None, image_dir=None)
        
        with (
            patch.object(cli, "_create_directory_if_not_exists") as mock_create_dir,
            patch("builtins.print") as mock_print,
        ):
            cli._apply_directory_overrides(args)

        assert cli.data_output_dir == original_data_dir
        assert cli.image_output_dir == original_image_dir
        assert cli.using_custom_data_dir is False
        assert cli.using_custom_image_dir is False
        mock_create_dir.assert_not_called()
        mock_print.assert_not_called()

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_sets_to_file_with_custom_data_dir(self, mock_json_dump, mock_file, cli):
        """Test saving sets with custom data directory (full override)."""
        cli.using_custom_data_dir = True
        cli.data_output_dir = os.path.join("custom", "data")
        mock_sets = [{"id": "set1", "name": "Test Set"}]

        with patch("builtins.print") as mock_print:
            cli._save_sets_to_file(mock_sets)

        # File should be saved directly to custom directory
        expected_path = os.path.join("custom", "data", "sets.json")
        mock_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
        mock_json_dump.assert_called_once_with(
            mock_sets,
            mock_file.return_value.__enter__.return_value,
            ensure_ascii=False,
            indent=2,
        )
        mock_print.assert_called_once_with(f"Sets data saved to {expected_path}")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_sets_to_file_with_default_data_dir(self, mock_json_dump, mock_file, cli):
        """Test saving sets with default data directory structure."""
        cli.using_custom_data_dir = False
        cli.data_output_dir = os.path.join("default", "data")
        mock_sets = [{"id": "set1", "name": "Test Set"}]

        with (
            patch.object(cli, "_create_directory_if_not_exists") as mock_create_dir,
            patch("builtins.print") as mock_print,
        ):
            cli._save_sets_to_file(mock_sets)

        # File should be saved to default lorcast subdirectory
        expected_dir = os.path.join("default", "data", "lorcast")
        expected_path = os.path.join(expected_dir, "sets.json")
        mock_create_dir.assert_called_once_with(expected_dir)
        mock_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
        mock_json_dump.assert_called_once_with(
            mock_sets,
            mock_file.return_value.__enter__.return_value,
            ensure_ascii=False,
            indent=2,
        )
        mock_print.assert_called_once_with(f"Sets data saved to {expected_path}")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_cards_to_file_with_custom_data_dir(self, mock_json_dump, mock_file, cli):
        """Test saving cards with custom data directory (full override)."""
        cli.using_custom_data_dir = True
        cli.data_output_dir = os.path.join("custom", "data")
        mock_cards = [{"id": "card1", "name": "Test Card"}]
        set_id = "test-set-123"

        with patch("builtins.print") as mock_print:
            cli._save_cards_to_file(mock_cards, set_id)

        # File should be saved directly to custom directory with set filename
        expected_path = os.path.join("custom", "data", "test-set-123.json")
        mock_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
        mock_json_dump.assert_called_once_with(
            mock_cards,
            mock_file.return_value.__enter__.return_value,
            ensure_ascii=False,
            indent=2,
        )
        mock_print.assert_called_once_with(f"Cards data saved to {expected_path}")

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_cards_to_file_with_default_data_dir(self, mock_json_dump, mock_file, cli):
        """Test saving cards with default data directory structure."""
        cli.using_custom_data_dir = False
        cli.data_output_dir = os.path.join("default", "data")
        mock_cards = [{"id": "card1", "name": "Test Card"}]
        set_id = "test-set-123"

        with (
            patch.object(cli, "_create_directory_if_not_exists") as mock_create_dir,
            patch("builtins.print") as mock_print,
        ):
            cli._save_cards_to_file(mock_cards, set_id)

        # File should be saved to default lorcast subdirectory structure
        expected_dir = os.path.join("default", "data", "lorcast", "sets")
        expected_path = os.path.join(expected_dir, "test-set-123.json")
        mock_create_dir.assert_called_once_with(expected_dir)
        mock_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
        mock_json_dump.assert_called_once_with(
            mock_cards,
            mock_file.return_value.__enter__.return_value,
            ensure_ascii=False,
            indent=2,
        )
        mock_print.assert_called_once_with(f"Cards data saved to {expected_path}")

    def test_download_card_images_with_custom_image_dir(self, cli, mock_lorcast_api):
        """Test downloading images with custom image directory (full override)."""
        cli.using_custom_image_dir = True
        cli.image_output_dir = os.path.join("custom", "images")
        mock_cards = [
            {"id": "card1", "image_uris": {"digital": {"normal": "http://example.com/card1.jpg"}}},
            {"id": "card2", "image_uris": {"digital": {"normal": "http://example.com/card2.jpg"}}}
        ]
        set_id = "test-set-123"

        with (
            patch.object(cli, "_download_single_card_image", return_value=True) as mock_download,
            patch("builtins.print") as mock_print,
        ):
            cli._download_card_images(mock_lorcast_api, mock_cards, set_id)

        # Images should be downloaded directly to custom directory
        expected_output_path = os.path.join("custom", "images")
        
        # Check that each card was downloaded to the custom directory
        expected_calls = [
            call(mock_lorcast_api, mock_cards[0], expected_output_path, "normal"),
            call(mock_lorcast_api, mock_cards[1], expected_output_path, "normal")
        ]
        mock_download.assert_has_calls(expected_calls)
        
        # Check success message
        mock_print.assert_any_call("Downloading images for 2 cards...")
        mock_print.assert_any_call("Successfully downloaded 2 out of 2 card images.")

    def test_download_card_images_with_default_image_dir(self, cli, mock_lorcast_api):
        """Test downloading images with default image directory structure."""
        cli.using_custom_image_dir = False
        cli.image_output_dir = os.path.join("default", "images")
        mock_cards = [
            {"id": "card1", "image_uris": {"digital": {"normal": "http://example.com/card1.jpg"}}}
        ]
        set_id = "test-set-123"

        with (
            patch.object(cli, "_create_directory_if_not_exists") as mock_create_dir,
            patch.object(cli, "_download_single_card_image", return_value=True) as mock_download,
            patch("builtins.print") as mock_print,
        ):
            cli._download_card_images(mock_lorcast_api, mock_cards, set_id)

        # Images should be downloaded to default lorcast subdirectory structure
        expected_output_path = os.path.join("default", "images", "lorcast", "sets", "test-set-123")
        mock_create_dir.assert_called_once_with(expected_output_path)
        mock_download.assert_called_once_with(
            mock_lorcast_api, mock_cards[0], expected_output_path, "normal"
        )

    @patch("inkcollector.cli.LorcastAPI")
    def test_handle_lorcast_command_applies_directory_overrides(self, mock_lorcast_class, cli):
        """Test that handle_lorcast_command applies directory overrides."""
        mock_lorcast = Mock()
        mock_lorcast_class.return_value = mock_lorcast

        args = argparse.Namespace(
            command="lorcast",
            lorcast_command="get-sets",
            output_dir="/custom/data",
            image_dir="/custom/images",
            json=False,
            save_json=False
        )

        with (
            patch.object(cli, "_apply_args_overrides") as mock_apply_args,
            patch.object(cli, "_apply_directory_overrides") as mock_apply_dirs,
            patch.object(cli, "_handle_get_sets_command") as mock_handle,
        ):
            cli.handle_lorcast_command(args)

        # Verify that directory overrides are applied
        mock_apply_args.assert_called_once_with(args)
        mock_apply_dirs.assert_called_once_with(args)
        mock_handle.assert_called_once_with(mock_lorcast, args)

    def test_mixed_custom_directories(self, cli):
        """Test behavior when only one custom directory is specified."""
        # Test custom data dir only
        args = argparse.Namespace(output_dir="/custom/data", image_dir=None)
        
        with (
            patch.object(cli, "_create_directory_if_not_exists"),
            patch("builtins.print"),
        ):
            cli._apply_directory_overrides(args)

        assert cli.using_custom_data_dir is True
        assert cli.using_custom_image_dir is False

        # Reset for next test
        cli.using_custom_data_dir = False
        cli.using_custom_image_dir = False

        # Test custom image dir only
        args = argparse.Namespace(output_dir=None, image_dir="/custom/images")
        
        with (
            patch.object(cli, "_create_directory_if_not_exists"),
            patch("builtins.print"),
        ):
            cli._apply_directory_overrides(args)

        assert cli.using_custom_data_dir is False
        assert cli.using_custom_image_dir is True

    @patch("inkcollector.cli.LorcastAPI")
    def test_end_to_end_custom_directories_get_sets(self, mock_lorcast_class, temp_dir):
        """Test end-to-end flow with custom directories for get-sets command."""
        # Setup mock
        mock_lorcast = Mock()
        mock_lorcast.get_sets.return_value = [{"id": "set1", "name": "Test Set"}]
        mock_lorcast_class.return_value = mock_lorcast

        # Create CLI with custom directories
        custom_data_dir = os.path.join(temp_dir, "custom_data")
        
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            cli = InkcollectorCLI()

        # Simulate command line arguments
        args = cli.parser.parse_args([
            "lorcast", "get-sets", 
            "--save-json",
            "--output-dir", custom_data_dir
        ])

        with (
            patch("builtins.open", mock_open()) as mock_file,
            patch("json.dump") as mock_json_dump,
            patch("builtins.print"),
        ):
            cli.handle_lorcast_command(args)

        # Verify that file was saved to custom directory (not lorcast subdirectory)
        expected_path = os.path.join(custom_data_dir, "sets.json")
        mock_file.assert_called_with(expected_path, "w", encoding="utf-8")

    @patch("inkcollector.cli.LorcastAPI")
    def test_end_to_end_custom_directories_get_cards(self, mock_lorcast_class, temp_dir):
        """Test end-to-end flow with custom directories for get-cards command."""
        # Setup mock
        mock_lorcast = Mock()
        mock_lorcast.get_set.return_value = {"id": "test-set"}
        mock_lorcast.get_cards.return_value = [
            {"id": "card1", "image_uris": {"digital": {"normal": "http://example.com/card1.jpg"}}}
        ]
        mock_lorcast_class.return_value = mock_lorcast

        # Create CLI with custom directories
        custom_data_dir = os.path.join(temp_dir, "custom_data")
        custom_image_dir = os.path.join(temp_dir, "custom_images")
        
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            cli = InkcollectorCLI()

        # Simulate command line arguments
        args = cli.parser.parse_args([
            "lorcast", "get-cards",
            "--set-id", "test-set",
            "--save-json",
            "--get-images",
            "--output-dir", custom_data_dir,
            "--image-dir", custom_image_dir
        ])

        with (
            patch("builtins.open", mock_open()) as mock_file,
            patch("json.dump") as mock_json_dump,
            patch.object(cli, "_download_single_card_image", return_value=True),
            patch("builtins.print"),
        ):
            cli.handle_lorcast_command(args)

        # Verify that card data was saved to custom directory (not lorcast subdirectory)
        expected_data_path = os.path.join(custom_data_dir, "test-set.json")
        mock_file.assert_called_with(expected_data_path, "w", encoding="utf-8")

    def test_custom_directories_with_workspace_override(self, cli):
        """Test that custom directories take precedence over workspace settings."""
        # Simulate workspace being applied first
        cli.data_output_dir = "/workspace/data"
        cli.image_output_dir = "/workspace/images"
        
        # Then apply custom directories
        custom_data_dir = os.path.abspath("/custom/data")
        custom_image_dir = os.path.abspath("/custom/images")
        args = argparse.Namespace(
            output_dir=custom_data_dir,
            image_dir=custom_image_dir
        )
        
        with (
            patch.object(cli, "_create_directory_if_not_exists"),
            patch("builtins.print"),
        ):
            cli._apply_directory_overrides(args)

        # Custom directories should override workspace settings
        assert cli.data_output_dir == custom_data_dir
        assert cli.image_output_dir == custom_image_dir
        assert cli.using_custom_data_dir is True
        assert cli.using_custom_image_dir is True
