"""
Test suite for the get-all-sets command functionality.

This module contains comprehensive tests for the get-all-sets command,
including argument parsing, command handling, bulk operations, error handling,
and all output options (JSON, save, images).
"""

import argparse
import os
import tempfile
from unittest.mock import Mock, call, patch

import pytest

from inkcollector.cli import InkcollectorCLI
from inkcollector.lorcast import LorcastAPI


class TestGetAllSetsCommand:
    """Test class for get-all-sets command functionality."""

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

    def test_parser_get_all_sets_command_exists(self, cli):
        """Test that get-all-sets command is available in parser."""
        args = cli.parser.parse_args(["lorcast", "get-all-sets"])
        assert args.command == "lorcast"
        assert args.lorcast_command == "get-all-sets"

    def test_parser_get_all_sets_arguments(self, cli):
        """Test get-all-sets command arguments parsing."""
        # Test basic command
        args = cli.parser.parse_args(["lorcast", "get-all-sets"])
        assert args.command == "lorcast"
        assert args.lorcast_command == "get-all-sets"
        assert args.json is False
        assert args.save_json is False
        assert args.get_images is None

        # Test with --json flag
        args = cli.parser.parse_args(["lorcast", "get-all-sets", "--json"])
        assert args.json is True

        # Test with --save-json flag
        args = cli.parser.parse_args(["lorcast", "get-all-sets", "--save-json"])
        assert args.save_json is True

        # Test with --get-images flag (default size)
        args = cli.parser.parse_args(["lorcast", "get-all-sets", "--get-images"])
        assert args.get_images == "normal"

        # Test with --get-images flag with specific size
        args = cli.parser.parse_args(["lorcast", "get-all-sets", "--get-images", "large"])
        assert args.get_images == "large"

        # Test with custom directories
        args = cli.parser.parse_args([
            "lorcast", "get-all-sets", 
            "--output-dir", "custom_data",
            "--image-dir", "custom_images"
        ])
        assert args.output_dir == "custom_data"
        assert args.image_dir == "custom_images"

        # Test with all options combined
        args = cli.parser.parse_args([
            "lorcast", "get-all-sets",
            "--json", "--save-json", "--get-images", "small",
            "--output-dir", "test_data", "--image-dir", "test_images"
        ])
        assert args.json is True
        assert args.save_json is True
        assert args.get_images == "small"
        assert args.output_dir == "test_data"
        assert args.image_dir == "test_images"

    def test_get_images_argument_choices(self, cli):
        """Test that get-images argument only accepts valid choices."""
        # Valid choices should work
        for size in ["small", "normal", "large"]:
            args = cli.parser.parse_args(["lorcast", "get-all-sets", "--get-images", size])
            assert args.get_images == size

        # Invalid choice should raise SystemExit
        with pytest.raises(SystemExit):
            cli.parser.parse_args(["lorcast", "get-all-sets", "--get-images", "invalid"])

    @patch("inkcollector.cli.LorcastAPI")
    def test_handle_lorcast_command_routes_to_get_all_sets(self, mock_lorcast_class, cli):
        """Test that lorcast command routes get-all-sets to the correct handler."""
        mock_lorcast = Mock()
        mock_lorcast_class.return_value = mock_lorcast

        args = argparse.Namespace(
            command="lorcast",
            lorcast_command="get-all-sets",
            json=False,
            save_json=False,
            get_images=None,
        )

        with patch.object(cli, "_handle_get_all_sets_command") as mock_handle:
            cli.handle_lorcast_command(args)

        mock_lorcast_class.assert_called_once()
        mock_handle.assert_called_once_with(mock_lorcast, args)

    def test_handle_get_all_sets_command_success(self, cli, mock_lorcast_api):
        """Test successful get-all-sets command handling."""
        args = argparse.Namespace(
            json=False,
            save_json=True,
            get_images=None,
        )

        with patch("builtins.print") as mock_print, \
             patch.object(cli, "_save_sets_to_file") as mock_save_sets, \
             patch.object(cli, "_save_cards_to_file") as mock_save_cards, \
             patch.object(cli, "_get_effective_profile") as mock_profile:
            
            # Mock profile to return basic settings
            mock_profile.return_value = Mock(
                print_json=False,
                save_json=True,
                extract_data=True,
                extract_images=False,
                image_size="normal"
            )
            
            cli._handle_get_all_sets_command(mock_lorcast_api, args)

        # Verify API calls
        mock_lorcast_api.get_sets.assert_called_once()
        assert mock_lorcast_api.get_cards.call_count == 3  # 3 sets

        # Verify print output
        expected_print_calls = [
            call("Fetching all sets and their cards..."),
            call("Found 3 sets."),
            call("\nProcessing set 1/3: First Set (ID: set1)"),
            call("Found 2 cards for set set1"),
            call("\nProcessing set 2/3: Second Set (ID: set2)"),
            call("Found 1 cards for set set2"),
            call("\nProcessing set 3/3: Third Set (ID: set3)"),
            call("Found 3 cards for set set3"),
        ]
        
        # Check some key print calls (order might vary due to summary)
        mock_print.assert_any_call("Fetching all sets and their cards...")
        mock_print.assert_any_call("Found 3 sets.")
        
        # Verify file saves
        mock_save_sets.assert_called_once()
        assert mock_save_cards.call_count == 3  # One for each set

    def test_handle_get_all_sets_command_no_sets(self, cli, mock_lorcast_api):
        """Test get-all-sets command when no sets are found."""
        mock_lorcast_api.get_sets.return_value = []

        args = argparse.Namespace(json=False, save_json=False, get_images=None)

        with patch("builtins.print") as mock_print:
            cli._handle_get_all_sets_command(mock_lorcast_api, args)

        mock_print.assert_any_call("No sets found.")
        mock_lorcast_api.get_cards.assert_not_called()

    def test_handle_get_all_sets_command_with_json_output(self, cli, mock_lorcast_api):
        """Test get-all-sets command with JSON output."""
        args = argparse.Namespace(
            json=True,
            save_json=False,
            get_images=None,
        )

        with patch.object(cli, "_print_sets_json") as mock_print_sets, \
             patch.object(cli, "_print_cards_json") as mock_print_cards, \
             patch.object(cli, "_get_effective_profile") as mock_profile:
            
            mock_profile.return_value = Mock(
                print_json=True,
                save_json=False,
                extract_data=True,
                extract_images=False,
                image_size="normal"
            )
            
            cli._handle_get_all_sets_command(mock_lorcast_api, args)

        # Verify JSON printing
        mock_print_sets.assert_called_once()
        assert mock_print_cards.call_count == 3  # One for each set

    def test_handle_get_all_sets_command_with_images(self, cli, mock_lorcast_api):
        """Test get-all-sets command with image download."""
        args = argparse.Namespace(
            json=False,
            save_json=False,
            get_images="large",
        )

        with patch.object(cli, "_download_card_images_bulk") as mock_download, \
             patch.object(cli, "_get_effective_profile") as mock_profile, \
             patch("builtins.print"):
            
            mock_profile.return_value = Mock(
                print_json=False,
                save_json=False,
                extract_data=True,
                extract_images=True,
                image_size="normal"
            )
            
            # Mock successful downloads
            mock_download.return_value = 2  # 2 successful downloads per set
            
            cli._handle_get_all_sets_command(mock_lorcast_api, args)

        # Verify image downloads for all sets
        assert mock_download.call_count == 3

    def test_handle_get_all_sets_command_set_without_id(self, cli, mock_lorcast_api):
        """Test get-all-sets command handles sets without ID gracefully."""
        # Mock sets with one missing ID
        mock_lorcast_api.get_sets.return_value = [
            {"id": "set1", "name": "First Set"},
            {"name": "Set Without ID"},  # Missing ID
            {"id": "set3", "name": "Third Set"},
        ]

        args = argparse.Namespace(json=False, save_json=False, get_images=None)

        with patch("builtins.print") as mock_print, \
             patch.object(cli, "_get_effective_profile") as mock_profile:
            
            mock_profile.return_value = Mock(
                print_json=False,
                save_json=False,
                extract_data=True,
                extract_images=False,
                image_size="normal"
            )
            
            cli._handle_get_all_sets_command(mock_lorcast_api, args)

        # Should skip the set without ID
        mock_print.assert_any_call("Set 2 has no ID, skipping...")
        # Should only call get_cards for sets with IDs (2 calls instead of 3)
        assert mock_lorcast_api.get_cards.call_count == 2

    def test_handle_get_all_sets_command_api_error(self, cli, mock_lorcast_api):
        """Test get-all-sets command handles API errors gracefully."""
        # Mock get_cards to raise an exception for one set
        def mock_get_cards_with_error(set_id):
            if set_id == "set2":
                raise Exception("API Error")
            return mock_lorcast_api.get_cards.side_effect(set_id)

        mock_lorcast_api.get_cards.side_effect = mock_get_cards_with_error

        args = argparse.Namespace(json=False, save_json=False, get_images=None)

        with patch("builtins.print") as mock_print, \
             patch.object(cli, "_get_effective_profile") as mock_profile:
            
            mock_profile.return_value = Mock(
                print_json=False,
                save_json=False,
                extract_data=True,
                extract_images=False,
                image_size="normal"
            )
            
            cli._handle_get_all_sets_command(mock_lorcast_api, args)

        # Should print error message and continue
        mock_print.assert_any_call("Error processing set set2: API Error")

    def test_handle_get_all_sets_command_empty_set(self, cli, mock_lorcast_api):
        """Test get-all-sets command handles empty sets."""
        # Mock one set to return no cards
        def mock_get_cards_empty(set_id):
            if set_id == "set2":
                return []
            return mock_lorcast_api.get_cards.side_effect(set_id)

        original_side_effect = mock_lorcast_api.get_cards.side_effect
        mock_lorcast_api.get_cards.side_effect = mock_get_cards_empty

        args = argparse.Namespace(json=False, save_json=False, get_images=None)

        with patch("builtins.print") as mock_print, \
             patch.object(cli, "_get_effective_profile") as mock_profile:
            
            mock_profile.return_value = Mock(
                print_json=False,
                save_json=False,
                extract_data=True,
                extract_images=False,
                image_size="normal"
            )
            
            cli._handle_get_all_sets_command(mock_lorcast_api, args)

        # Should handle empty set gracefully
        mock_print.assert_any_call("No cards found for set set2")

    def test_download_card_images_bulk_success(self, cli, mock_lorcast_api):
        """Test bulk image download functionality."""
        cards = [
            {"id": "card1", "image_uris": {"digital": {"normal": "http://example.com/1.jpg"}}},
            {"id": "card2", "image_uris": {"digital": {"normal": "http://example.com/2.jpg"}}},
        ]

        with patch.object(cli, "_download_single_card_image") as mock_download_single, \
             patch.object(cli, "_create_directory_if_not_exists") as mock_create_dir, \
             patch("builtins.print") as mock_print:
            
            # Mock successful downloads
            mock_download_single.return_value = True
            
            result = cli._download_card_images_bulk(mock_lorcast_api, cards, "test_set", "normal")

        assert result == 2  # Both downloads successful
        assert mock_download_single.call_count == 2
        mock_print.assert_any_call("  Successfully downloaded 2/2 images")

    def test_download_card_images_bulk_partial_success(self, cli, mock_lorcast_api):
        """Test bulk image download with some failures."""
        cards = [
            {"id": "card1", "image_uris": {"digital": {"normal": "http://example.com/1.jpg"}}},
            {"id": "card2", "image_uris": {"digital": {"normal": "http://example.com/2.jpg"}}},
        ]

        with patch.object(cli, "_download_single_card_image") as mock_download_single, \
             patch.object(cli, "_create_directory_if_not_exists") as mock_create_dir, \
             patch("builtins.print") as mock_print:
            
            # Mock one success, one failure
            mock_download_single.side_effect = [True, False]
            
            result = cli._download_card_images_bulk(mock_lorcast_api, cards, "test_set", "normal")

        assert result == 1  # Only one download successful
        mock_print.assert_any_call("  Successfully downloaded 1/2 images")

    def test_download_card_images_bulk_custom_directory(self, cli, mock_lorcast_api):
        """Test bulk image download with custom directory."""
        cli.using_custom_image_dir = True
        cli.image_output_dir = "/custom/images"
        
        cards = [{"id": "card1", "image_uris": {"digital": {"normal": "http://example.com/1.jpg"}}}]

        with patch.object(cli, "_download_single_card_image") as mock_download_single, \
             patch("builtins.print"):
            
            mock_download_single.return_value = True
            cli._download_card_images_bulk(mock_lorcast_api, cards, "test_set", "normal")

        # Should use custom directory, not create subdirectories
        expected_path = "/custom/images"
        mock_download_single.assert_called_with(
            mock_lorcast_api, cards[0], expected_path, "normal"
        )

    def test_effective_profile_integration(self, cli, mock_lorcast_api):
        """Test that get-all-sets respects profile settings when no command line overrides."""
        # Create args without get_images attribute to trigger profile fallback
        args = argparse.Namespace(
            json=False,  # Not explicitly set to True
            save_json=False,  # Not explicitly set to True
        )
        # Don't add get_images attribute to test profile fallback

        # Mock profile with specific settings
        mock_profile = Mock(
            print_json=True,  # Profile wants JSON
            save_json=True,   # Profile wants save
            extract_data=True,
            extract_images=True,  # Profile wants images
            image_size="large"    # Profile specifies large images
        )

        with patch.object(cli, "_get_effective_profile", return_value=mock_profile), \
             patch.object(cli, "_print_sets_json") as mock_print_sets, \
             patch.object(cli, "_print_cards_json") as mock_print_cards, \
             patch.object(cli, "_save_sets_to_file") as mock_save_sets, \
             patch.object(cli, "_save_cards_to_file") as mock_save_cards, \
             patch.object(cli, "_download_card_images_bulk") as mock_download, \
             patch("builtins.print"):
            
            mock_download.return_value = 1
            cli._handle_get_all_sets_command(mock_lorcast_api, args)

        # Should use profile settings since args don't override
        mock_print_sets.assert_called_once()  # Profile print_json=True
        mock_save_sets.assert_called_once()   # Profile save_json=True and extract_data=True
        # Images: hasattr(args, "get_images") is False, so profile.extract_images=True applies
        assert mock_download.call_count == 3   # Images enabled for all sets

    def test_command_line_overrides_profile(self, cli, mock_lorcast_api):
        """Test that command line arguments override profile settings."""
        args = argparse.Namespace(
            json=True,         # Explicitly set to True (this overrides profile)
            save_json=True,    # Explicitly set to True (this overrides profile)
            get_images="small",  # Explicitly set to small (this overrides profile)
        )

        # Mock profile with different settings
        mock_profile = Mock(
            print_json=False,    # Profile doesn't want JSON
            save_json=False,     # Profile doesn't want save
            extract_data=True,
            extract_images=False,  # Profile doesn't want images
            image_size="large"     # Profile specifies large images
        )

        with patch.object(cli, "_get_effective_profile", return_value=mock_profile), \
             patch.object(cli, "_print_sets_json") as mock_print_sets, \
             patch.object(cli, "_save_sets_to_file") as mock_save_sets, \
             patch.object(cli, "_download_card_images_bulk") as mock_download, \
             patch("builtins.print"):
            
            mock_download.return_value = 1
            cli._handle_get_all_sets_command(mock_lorcast_api, args)

        # Should use command line overrides
        mock_print_sets.assert_called_once()    # args.json=True overrides profile
        mock_save_sets.assert_called_once()     # args.save_json=True overrides profile
        assert mock_download.call_count == 3    # args.get_images="small" overrides profile
        
        # Verify image size override
        for call_args in mock_download.call_args_list:
            assert call_args[0][3] == "small"  # Fourth argument is image_size

    def test_profile_with_get_images_none(self, cli, mock_lorcast_api):
        """Test profile behavior when get_images is explicitly None."""
        args = argparse.Namespace(
            json=False,
            save_json=False,
            get_images=None,  # Explicitly set to None
        )

        mock_profile = Mock(
            print_json=False,
            save_json=False,
            extract_data=True,
            extract_images=True,  # Profile wants images
            image_size="normal"
        )

        with patch.object(cli, "_get_effective_profile", return_value=mock_profile), \
             patch.object(cli, "_download_card_images_bulk") as mock_download, \
             patch("builtins.print"):
            
            mock_download.return_value = 1
            cli._handle_get_all_sets_command(mock_lorcast_api, args)

        # Since args.get_images is None (which is not "not None") and hasattr(args, "get_images") is True,
        # should_download_images = False
        assert mock_download.call_count == 0
