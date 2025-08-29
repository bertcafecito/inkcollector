"""
Test error scenarios and edge cases for the CLI.

This module tests various error conditions, edge cases, and error handling
in the inkcollector CLI.
"""

import os
from unittest.mock import Mock, mock_open, patch

import pytest
from requests.exceptions import ConnectionError, Timeout

from inkcollector.cli import InkcollectorCLI


class TestErrorScenarios:
    """Test error scenarios and edge cases."""

    @pytest.fixture
    def cli_with_temp_dirs(self, temp_directory):
        """Create CLI instance with temporary directories."""
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            cli = InkcollectorCLI()
            cli.data_output_dir = os.path.join(temp_directory, "data")
            cli.image_output_dir = os.path.join(temp_directory, "images")
            return cli

    def test_lorcast_api_connection_error(self, cli_with_temp_dirs):
        """Test handling of API connection errors."""
        with patch("inkcollector.cli.LorcastAPI") as mock_lorcast_class:
            mock_lorcast = Mock()
            mock_lorcast.get_sets.side_effect = ConnectionError("Connection failed")
            mock_lorcast_class.return_value = mock_lorcast

            args = mock_parse_args(lorcast_command="get-sets")

            with pytest.raises(ConnectionError):
                cli_with_temp_dirs.handle_lorcast_command(args)

    def test_lorcast_api_timeout_error(self, cli_with_temp_dirs):
        """Test handling of API timeout errors."""
        with patch("inkcollector.cli.LorcastAPI") as mock_lorcast_class:
            mock_lorcast = Mock()
            mock_lorcast.get_cards.side_effect = Timeout("Request timed out")
            mock_lorcast.get_set.return_value = {"id": "set1"}
            mock_lorcast_class.return_value = mock_lorcast

            args = mock_parse_args(lorcast_command="get-cards", set_id="set1")

            with pytest.raises(Timeout):
                cli_with_temp_dirs.handle_lorcast_command(args)

    def test_json_dump_error_in_save_sets(self, cli_with_temp_dirs):
        """Test JSON serialization error when saving sets."""
        mock_sets = [
            {"id": "set1", "invalid_data": object()}
        ]  # Non-serializable object

        with (
            patch("builtins.open", mock_open()),
            patch("json.dump", side_effect=TypeError("Object not serializable")),
            patch.object(cli_with_temp_dirs, "_create_directory_if_not_exists"),
            patch("builtins.print") as mock_print,
        ):

            cli_with_temp_dirs._save_sets_to_file(mock_sets)

            # Should print error message
            error_calls = [
                call
                for call in mock_print.call_args_list
                if "Error saving" in str(call)
            ]
            assert len(error_calls) > 0

    def test_json_dump_error_in_save_cards(self, cli_with_temp_dirs):
        """Test JSON serialization error when saving cards."""
        mock_cards = [
            {"id": "card1", "invalid_data": object()}
        ]  # Non-serializable object
        set_id = "test-set"

        with (
            patch("builtins.open", mock_open()),
            patch("json.dump", side_effect=TypeError("Object not serializable")),
            patch.object(cli_with_temp_dirs, "_create_directory_if_not_exists"),
            patch("builtins.print") as mock_print,
        ):

            cli_with_temp_dirs._save_cards_to_file(mock_cards, set_id)

            # Should print error message
            error_calls = [
                call
                for call in mock_print.call_args_list
                if "Error saving" in str(call)
            ]
            assert len(error_calls) > 0

    def test_file_permission_error_in_save_sets(self, cli_with_temp_dirs):
        """Test file permission error when saving sets."""
        mock_sets = [{"id": "set1", "name": "Test Set"}]

        with (
            patch("builtins.open", side_effect=PermissionError("Permission denied")),
            patch.object(cli_with_temp_dirs, "_create_directory_if_not_exists"),
            patch("builtins.print") as mock_print,
        ):

            cli_with_temp_dirs._save_sets_to_file(mock_sets)

            mock_print.assert_any_call(
                f"Error saving sets data to "
                f"{os.path.join(cli_with_temp_dirs.data_output_dir, cli_with_temp_dirs.LORCAST_DATASOURCE_DIR, 'sets.json')}: "  # noqa: E501
                "Permission denied"
            )

    def test_directory_creation_error(self, cli_with_temp_dirs):
        """Test error in directory creation."""
        with (
            patch("os.path.exists", return_value=False),
            patch("os.makedirs", side_effect=OSError("Cannot create directory")),
            pytest.raises(OSError),
        ):

            cli_with_temp_dirs._create_directory_if_not_exists("test_dir")

    def test_card_image_download_partial_failure(self, cli_with_temp_dirs):
        """Test partial failure in card image downloads."""
        mock_lorcast = Mock()
        mock_cards = [
            {
                "id": "card1",
                "image_uris": {"digital": {"normal": "http://example.com/card1.jpg"}},
            },
            {
                "id": "card2",
                "image_uris": {"digital": {"normal": "http://example.com/card2.jpg"}},
            },
            {"id": "card3"},  # Missing image_uris
        ]

        # First download succeeds, second fails, third has no image URIs
        def download_side_effect(url, path):
            if "card2" in path:
                raise Exception("Download failed")

        mock_lorcast.download_image.side_effect = download_side_effect

        with (
            patch.object(cli_with_temp_dirs, "_create_directory_if_not_exists"),
            patch("builtins.print") as mock_print,
        ):

            cli_with_temp_dirs._download_card_images(mock_lorcast, mock_cards, "set1")

            # Should report 1 successful download out of 3 cards
            mock_print.assert_any_call(
                "Successfully downloaded 1 out of 3 card images."
            )

    def test_card_with_missing_digital_image_uris(self, cli_with_temp_dirs):
        """Test card with missing digital image URIs structure."""
        mock_lorcast = Mock()
        mock_card = {
            "id": "card1",
            "image_uris": {
                "physical": {"normal": "http://example.com/physical.jpg"}
                # Missing 'digital' key
            },
        }

        with patch("builtins.print") as mock_print:
            result = cli_with_temp_dirs._download_single_card_image(
                mock_lorcast, mock_card, "/test/path"
            )

        assert result is False
        mock_print.assert_called_once_with(
            "No digital image URIs found for card card1, skipping image download."
        )

    def test_card_with_missing_image_size(self, cli_with_temp_dirs):
        """Test card with missing specific image size."""
        mock_lorcast = Mock()
        mock_card = {
            "id": "card1",
            "image_uris": {
                "digital": {
                    "small": "http://example.com/small.jpg"
                    # Missing 'normal' and 'large'
                }
            },
        }

        with patch("builtins.print") as mock_print:
            result = cli_with_temp_dirs._download_single_card_image(
                mock_lorcast, mock_card, "/test/path", "large"  # Request 'large' size
            )

        assert result is False
        mock_print.assert_called_once_with(
            "No large image URI found for card card1, skipping image download."
        )

    def test_empty_sets_response(self, cli_with_temp_dirs):
        """Test handling of empty sets response."""
        mock_lorcast = Mock()
        mock_lorcast.get_sets.return_value = []

        args = mock_parse_args(lorcast_command="get-sets", json=True, save_json=True)

        with patch("builtins.print") as mock_print:
            cli_with_temp_dirs._handle_get_sets_command(mock_lorcast, args)

        mock_print.assert_any_call("No sets found.")
        # Should not try to print or save empty data

    def test_empty_cards_response(self, cli_with_temp_dirs):
        """Test handling of empty cards response."""
        mock_lorcast = Mock()
        mock_lorcast.get_set.return_value = {"id": "set1"}
        mock_lorcast.get_cards.return_value = []

        args = mock_parse_args(
            lorcast_command="get-cards",
            set_id="set1",
            json=True,
            save_json=True,
            get_images="normal",
        )

        with patch("builtins.print") as mock_print:
            cli_with_temp_dirs._handle_get_cards_command(mock_lorcast, args)

        mock_print.assert_any_call("Found 0 cards for set id set1.")

    def test_malformed_set_response(self, cli_with_temp_dirs):
        """Test handling of malformed set response."""
        mock_lorcast = Mock()
        mock_lorcast.get_set.return_value = {"name": "Test Set"}  # Missing 'id' field

        args = mock_parse_args(lorcast_command="get-cards", set_id="invalid")

        with patch("builtins.print") as mock_print:
            cli_with_temp_dirs._handle_get_cards_command(mock_lorcast, args)

        mock_print.assert_any_call("Set with id invalid not found.")
        mock_lorcast.get_cards.assert_not_called()

    def test_invalid_command_line_arguments(self):
        """Test handling of invalid command line arguments."""
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            cli = InkcollectorCLI()

            # Test missing required argument
            with pytest.raises(SystemExit):
                cli.parser.parse_args(["lorcast", "get-cards"])  # Missing --set-id

            # Test invalid image size
            with pytest.raises(SystemExit):
                cli.parser.parse_args(
                    [
                        "lorcast",
                        "get-cards",
                        "--set-id",
                        "test",
                        "--get-images",
                        "invalid-size",
                    ]
                )

    def test_unicode_handling_in_file_operations(self, cli_with_temp_dirs):
        """Test Unicode handling in file save operations."""
        mock_sets = [
            {
                "id": "set1",
                "name": "Tëst Sét wïth Ünïcödë",
                "description": "Descripción en español",
            }
        ]

        with (
            patch("builtins.open", mock_open()) as mock_file,
            patch("json.dump") as mock_json_dump,
            patch.object(cli_with_temp_dirs, "_create_directory_if_not_exists"),
        ):

            cli_with_temp_dirs._save_sets_to_file(mock_sets)

            # Verify file opened with UTF-8 encoding
            mock_file.assert_called_once()
            call_args = mock_file.call_args
            assert "encoding" in call_args[1]
            assert call_args[1]["encoding"] == "utf-8"

            # Verify JSON dump called with ensure_ascii=False
            mock_json_dump.assert_called_once()
            call_args = mock_json_dump.call_args
            assert call_args[1]["ensure_ascii"] is False


def mock_parse_args(**kwargs):
    """Helper function to create mock parsed arguments."""
    from argparse import Namespace

    defaults = {
        "command": "lorcast",
        "lorcast_command": None,
        "json": False,
        "save_json": False,
        "set_id": None,
        "get_images": None,
    }
    defaults.update(kwargs)
    return Namespace(**defaults)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_very_large_dataset_handling(self):
        """Test handling of very large datasets."""
        # This would be a performance test in a real scenario
        large_sets = [{"id": f"set{i}", "name": f"Set {i}"} for i in range(1000)]

        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            cli = InkcollectorCLI()

        # Should not crash with large datasets
        with patch("builtins.print"), patch("json.dumps", return_value="mock_json"):
            cli._print_sets_json(large_sets)

    def test_special_characters_in_paths(self, temp_directory):
        """Test handling of special characters in file paths."""
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            cli = InkcollectorCLI()

        # Test with path containing special characters
        special_path = os.path.join(temp_directory, "test & data", "special#chars")

        with (
            patch("os.path.exists", return_value=False),
            patch("os.makedirs") as mock_makedirs,
            patch("builtins.print"),
        ):

            cli._create_directory_if_not_exists(special_path)
            mock_makedirs.assert_called_once_with(special_path)

    def test_concurrent_access_scenarios(self, cli_args_sets_save, temp_directory):
        """Test scenarios that might involve concurrent access."""
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            cli = InkcollectorCLI()
            cli.data_output_dir = temp_directory

        mock_sets = [{"id": "set1", "name": "Test Set"}]

        # Simulate file being locked/in use
        with (
            patch("builtins.open", side_effect=OSError("File in use")),
            patch.object(cli, "_create_directory_if_not_exists"),
            patch("builtins.print") as mock_print,
        ):

            cli._save_sets_to_file(mock_sets)

            # Should handle the error gracefully
            error_calls = [
                call
                for call in mock_print.call_args_list
                if "Error saving" in str(call)
            ]
            assert len(error_calls) > 0
