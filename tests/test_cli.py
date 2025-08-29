"""
Test suite for the inkcollector CLI module.

This module contains comprehensive tests for the InkcollectorCLI class,
including argument parsing, command handling, directory creation, file operations,
and error handling scenarios.
"""

import argparse
import os
import tempfile
from unittest.mock import Mock, call, mock_open, patch

import pytest

from inkcollector.cli import InkcollectorCLI, main
from inkcollector.lorcast import LorcastAPI


class TestInkcollectorCLI:
    """Test class for InkcollectorCLI functionality."""

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
            return cli

    @pytest.fixture
    def mock_lorcast_api(self):
        """Create a mock LorcastAPI instance."""
        return Mock(spec=LorcastAPI)

    def test_init_creates_parser(self):
        """Test that CLI initialization creates an argument parser."""
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            cli = InkcollectorCLI()
            assert cli.parser is not None
            assert isinstance(cli.parser, argparse.ArgumentParser)

    def test_init_sets_default_directories(self):
        """Test that CLI initialization sets default directory paths."""
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            cli = InkcollectorCLI()
            assert cli.data_output_dir == "data"
            assert cli.image_output_dir == "images"

    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_create_directory_if_not_exists_creates_new_directory(
        self, mock_exists, mock_makedirs, cli
    ):
        """Test directory creation when directory doesn't exist."""
        mock_exists.return_value = False

        with patch("builtins.print") as mock_print:
            cli._create_directory_if_not_exists("test_dir")

        mock_makedirs.assert_called_once_with("test_dir")
        mock_print.assert_called_once_with("Created directory: test_dir")

    @patch("os.makedirs")
    @patch("os.path.exists")
    def test_create_directory_if_not_exists_skips_existing_directory(
        self, mock_exists, mock_makedirs, cli
    ):
        """Test that existing directories are not recreated."""
        mock_exists.return_value = True

        cli._create_directory_if_not_exists("existing_dir")

        mock_makedirs.assert_not_called()

    def test_parser_has_version_argument(self, cli):
        """Test that the parser includes version argument."""
        # Testing version would normally exit, so we'll check the parser setup
        actions = [action for action in cli.parser._actions if action.dest == "version"]
        assert len(actions) == 1
        assert actions[0].option_strings == ["-v", "--version"]

    def test_parser_has_lorcast_command(self, cli):
        """Test that the parser includes lorcast command."""
        # Parse valid lorcast command
        args = cli.parser.parse_args(["lorcast", "get-sets"])
        assert args.command == "lorcast"
        assert args.lorcast_command == "get-sets"

    def test_parser_lorcast_get_sets_arguments(self, cli):
        """Test lorcast get-sets command arguments."""
        # Test with --json flag
        args = cli.parser.parse_args(["lorcast", "get-sets", "--json"])
        assert args.command == "lorcast"
        assert args.lorcast_command == "get-sets"
        assert args.json is True
        assert args.save_json is False

        # Test with --save-json flag
        args = cli.parser.parse_args(["lorcast", "get-sets", "--save-json"])
        assert args.save_json is True
        assert args.json is False

        # Test with both flags
        args = cli.parser.parse_args(["lorcast", "get-sets", "--json", "--save-json"])
        assert args.json is True
        assert args.save_json is True

    def test_parser_lorcast_get_cards_arguments(self, cli):
        """Test lorcast get-cards command arguments."""
        # Test required set-id argument
        args = cli.parser.parse_args(["lorcast", "get-cards", "--set-id", "test-set"])
        assert args.command == "lorcast"
        assert args.lorcast_command == "get-cards"
        assert args.set_id == "test-set"
        assert args.json is False
        assert args.save_json is False
        assert args.get_images is None

        # Test with image download options
        args = cli.parser.parse_args(
            ["lorcast", "get-cards", "--set-id", "test-set", "--get-images"]
        )
        assert args.get_images == "normal"  # Default size

        args = cli.parser.parse_args(
            ["lorcast", "get-cards", "--set-id", "test-set", "--get-images", "large"]
        )
        assert args.get_images == "large"

    def test_parser_requires_set_id_for_get_cards(self, cli):
        """Test that get-cards command requires set-id argument."""
        with pytest.raises(SystemExit):
            cli.parser.parse_args(["lorcast", "get-cards"])

    def test_handle_lorcast_command_no_subcommand(self, cli):
        """Test lorcast command handling when no subcommand is provided."""
        args = argparse.Namespace(command="lorcast")

        with patch("builtins.print") as mock_print:
            cli.handle_lorcast_command(args)

        mock_print.assert_called_once_with(
            "Lorcast command is under development. "
            "Use --help to see available subcommands."
        )

    @patch("inkcollector.cli.LorcastAPI")
    def test_handle_lorcast_command_get_sets(self, mock_lorcast_class, cli):
        """Test lorcast get-sets command handling."""
        mock_lorcast = Mock()
        mock_lorcast_class.return_value = mock_lorcast

        args = argparse.Namespace(
            command="lorcast", lorcast_command="get-sets", json=False, save_json=False
        )

        with patch.object(cli, "_handle_get_sets_command") as mock_handle:
            cli.handle_lorcast_command(args)

        mock_lorcast_class.assert_called_once()
        mock_handle.assert_called_once_with(mock_lorcast, args)

    @patch("inkcollector.cli.LorcastAPI")
    def test_handle_lorcast_command_get_cards(self, mock_lorcast_class, cli):
        """Test lorcast get-cards command handling."""
        mock_lorcast = Mock()
        mock_lorcast_class.return_value = mock_lorcast

        args = argparse.Namespace(
            command="lorcast",
            lorcast_command="get-cards",
            set_id="test-set",
            json=False,
            save_json=False,
            get_images=None,
        )

        with patch.object(cli, "_handle_get_cards_command") as mock_handle:
            cli.handle_lorcast_command(args)

        mock_lorcast_class.assert_called_once()
        mock_handle.assert_called_once_with(mock_lorcast, args)

    @patch("inkcollector.cli.LorcastAPI")
    def test_handle_lorcast_command_unknown_subcommand(self, mock_lorcast_class, cli):
        """Test handling of unknown lorcast subcommand."""
        args = argparse.Namespace(command="lorcast", lorcast_command="unknown-command")

        with patch("builtins.print") as mock_print:
            cli.handle_lorcast_command(args)

        mock_print.assert_called_once_with(
            "Unknown lorcast subcommand: unknown-command"
        )

    def test_handle_get_sets_command_success(self, cli, mock_lorcast_api):
        """Test successful get-sets command handling."""
        mock_sets = [
            {"id": "set1", "name": "Test Set 1"},
            {"id": "set2", "name": "Test Set 2"},
        ]
        mock_lorcast_api.get_sets.return_value = mock_sets

        args = argparse.Namespace(json=False, save_json=False)

        with patch("builtins.print") as mock_print:
            cli._handle_get_sets_command(mock_lorcast_api, args)

        mock_lorcast_api.get_sets.assert_called_once()
        expected_calls = [call("Fetching sets data..."), call("Found 2 sets.")]
        mock_print.assert_has_calls(expected_calls)

    def test_handle_get_sets_command_no_sets(self, cli, mock_lorcast_api):
        """Test get-sets command when no sets are found."""
        mock_lorcast_api.get_sets.return_value = []

        args = argparse.Namespace(json=False, save_json=False)

        with patch("builtins.print") as mock_print:
            cli._handle_get_sets_command(mock_lorcast_api, args)

        mock_print.assert_any_call("No sets found.")

    def test_handle_get_sets_command_with_json_output(self, cli, mock_lorcast_api):
        """Test get-sets command with JSON output."""
        mock_sets = [{"id": "set1", "name": "Test Set 1"}]
        mock_lorcast_api.get_sets.return_value = mock_sets

        args = argparse.Namespace(json=True, save_json=False)

        with patch.object(cli, "_print_sets_json") as mock_print_json:
            cli._handle_get_sets_command(mock_lorcast_api, args)

        mock_print_json.assert_called_once_with(mock_sets)

    def test_handle_get_sets_command_with_save_json(self, cli, mock_lorcast_api):
        """Test get-sets command with save JSON option."""
        mock_sets = [{"id": "set1", "name": "Test Set 1"}]
        mock_lorcast_api.get_sets.return_value = mock_sets

        args = argparse.Namespace(json=False, save_json=True)

        with patch.object(cli, "_save_sets_to_file") as mock_save:
            cli._handle_get_sets_command(mock_lorcast_api, args)

        mock_save.assert_called_once_with(mock_sets)

    def test_handle_get_cards_command_success(self, cli, mock_lorcast_api):
        """Test successful get-cards command handling."""
        mock_set = {"id": "set1", "name": "Test Set"}
        mock_cards = [
            {"id": "card1", "name": "Test Card 1"},
            {"id": "card2", "name": "Test Card 2"},
        ]
        mock_lorcast_api.get_set.return_value = mock_set
        mock_lorcast_api.get_cards.return_value = mock_cards

        args = argparse.Namespace(
            set_id="set1", json=False, save_json=False, get_images=None
        )

        with patch("builtins.print") as mock_print:
            cli._handle_get_cards_command(mock_lorcast_api, args)

        mock_lorcast_api.get_set.assert_called_once_with("set1")
        mock_lorcast_api.get_cards.assert_called_once_with("set1")
        mock_print.assert_any_call("Found 2 cards for set id set1.")

    def test_handle_get_cards_command_set_not_found(self, cli, mock_lorcast_api):
        """Test get-cards command when set is not found."""
        mock_lorcast_api.get_set.return_value = {}  # No id in response

        args = argparse.Namespace(set_id="nonexistent")

        with patch("builtins.print") as mock_print:
            cli._handle_get_cards_command(mock_lorcast_api, args)

        mock_print.assert_any_call("Set with id nonexistent not found.")
        mock_lorcast_api.get_cards.assert_not_called()

    def test_handle_get_cards_command_with_images(self, cli, mock_lorcast_api):
        """Test get-cards command with image download."""
        mock_set = {"id": "set1", "name": "Test Set"}
        mock_cards = [{"id": "card1", "name": "Test Card 1"}]
        mock_lorcast_api.get_set.return_value = mock_set
        mock_lorcast_api.get_cards.return_value = mock_cards

        args = argparse.Namespace(
            set_id="set1", json=False, save_json=False, get_images="large"
        )

        with patch.object(cli, "_download_card_images") as mock_download:
            cli._handle_get_cards_command(mock_lorcast_api, args)

        mock_download.assert_called_once_with(
            mock_lorcast_api, mock_cards, "set1", "large"
        )

    def test_print_sets_json(self, cli):
        """Test printing sets as JSON."""
        mock_sets = [{"id": "set1", "name": "Test Set"}]

        with (
            patch("builtins.print") as mock_print,
            patch("json.dumps") as mock_json_dumps,
        ):
            mock_json_dumps.return_value = '{"test": "json"}'

            cli._print_sets_json(mock_sets)

            mock_json_dumps.assert_called_once_with(mock_sets, indent=2)
            # Check that print was called with headers and JSON
            assert mock_print.call_count >= 4

    def test_print_cards_json(self, cli):
        """Test printing cards as JSON."""
        mock_cards = [{"id": "card1", "name": "Test Card"}]
        set_id = "test-set"

        with (
            patch("builtins.print") as mock_print,
            patch("json.dumps") as mock_json_dumps,
        ):
            mock_json_dumps.return_value = '{"test": "json"}'

            cli._print_cards_json(mock_cards, set_id)

            mock_json_dumps.assert_called_once_with(mock_cards, indent=2)
            assert mock_print.call_count >= 4

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_sets_to_file_success(self, mock_json_dump, mock_file, cli):
        """Test successful saving of sets to file."""
        mock_sets = [{"id": "set1", "name": "Test Set"}]

        with (
            patch.object(cli, "_create_directory_if_not_exists") as mock_create_dir,
            patch("builtins.print"),
        ):

            cli._save_sets_to_file(mock_sets)

            mock_create_dir.assert_called_once()
            mock_file.assert_called_once()
            mock_json_dump.assert_called_once_with(
                mock_sets,
                mock_file.return_value.__enter__.return_value,
                ensure_ascii=False,
                indent=2,
            )

    @patch("builtins.open", side_effect=Exception("File error"))
    def test_save_sets_to_file_error(self, mock_file, cli):
        """Test error handling when saving sets to file."""
        mock_sets = [{"id": "set1", "name": "Test Set"}]

        with (
            patch.object(cli, "_create_directory_if_not_exists"),
            patch("builtins.print") as mock_print,
        ):

            cli._save_sets_to_file(mock_sets)

            mock_print.assert_any_call(
                f"Error saving sets data to "
                f"{os.path.join(cli.data_output_dir, cli.LORCAST_DATASOURCE_DIR, 'sets.json')}: "  # noqa: E501
                "File error"
            )

    @patch("builtins.open", new_callable=mock_open)
    @patch("json.dump")
    def test_save_cards_to_file_success(self, mock_json_dump, mock_file, cli):
        """Test successful saving of cards to file."""
        mock_cards = [{"id": "card1", "name": "Test Card"}]
        set_id = "test-set"

        with (
            patch.object(cli, "_create_directory_if_not_exists") as mock_create_dir,
            patch("builtins.print"),
        ):

            cli._save_cards_to_file(mock_cards, set_id)

            mock_create_dir.assert_called_once()
            mock_file.assert_called_once()
            mock_json_dump.assert_called_once_with(
                mock_cards,
                mock_file.return_value.__enter__.return_value,
                ensure_ascii=False,
                indent=2,
            )

    def test_download_card_images(self, cli, mock_lorcast_api):
        """Test downloading card images."""
        mock_cards = [
            {"id": "card1", "name": "Test Card 1"},
            {"id": "card2", "name": "Test Card 2"},
        ]
        set_id = "test-set"

        with (
            patch.object(cli, "_create_directory_if_not_exists"),
            patch.object(
                cli, "_download_single_card_image", return_value=True
            ) as mock_download_single,
            patch("builtins.print") as mock_print,
        ):

            cli._download_card_images(mock_lorcast_api, mock_cards, set_id)

            assert mock_download_single.call_count == 2
            mock_print.assert_any_call(
                "Successfully downloaded 2 out of 2 card images."
            )

    def test_download_single_card_image_success(self, cli, mock_lorcast_api):
        """Test successful single card image download."""
        mock_card = {
            "id": "card1",
            "image_uris": {"digital": {"normal": "http://example.com/image.jpg"}},
        }
        output_path = "/test/path"

        result = cli._download_single_card_image(
            mock_lorcast_api, mock_card, output_path
        )

        assert result is True
        mock_lorcast_api.download_image.assert_called_once_with(
            "http://example.com/image.jpg", os.path.join(output_path, "crd_card1.jpg")
        )

    def test_download_single_card_image_no_id(self, cli, mock_lorcast_api):
        """Test single card image download with missing card ID."""
        mock_card = {"name": "Test Card"}  # No id

        with patch("builtins.print") as mock_print:
            result = cli._download_single_card_image(
                mock_lorcast_api, mock_card, "/test/path"
            )

        assert result is False
        mock_print.assert_called_once_with(
            "Card ID not found, skipping image download."
        )

    def test_download_single_card_image_no_image_uris(self, cli, mock_lorcast_api):
        """Test single card image download with missing image URIs."""
        mock_card = {"id": "card1", "name": "Test Card"}  # No image_uris

        with patch("builtins.print") as mock_print:
            result = cli._download_single_card_image(
                mock_lorcast_api, mock_card, "/test/path"
            )

        assert result is False
        mock_print.assert_called_once_with(
            "No image URIs found for card card1, skipping image download."
        )

    def test_download_single_card_image_download_error(self, cli, mock_lorcast_api):
        """Test single card image download with download error."""
        mock_card = {
            "id": "card1",
            "image_uris": {"digital": {"normal": "http://example.com/image.jpg"}},
        }
        mock_lorcast_api.download_image.side_effect = Exception("Download failed")

        with patch("builtins.print") as mock_print:
            result = cli._download_single_card_image(
                mock_lorcast_api, mock_card, "/test/path"
            )

        assert result is False
        mock_print.assert_called_once_with(
            "Error downloading image for card card1: Download failed"
        )

    def test_run_with_lorcast_command(self, cli):
        """Test running CLI with lorcast command."""
        with (
            patch.object(cli.parser, "parse_args") as mock_parse,
            patch.object(cli, "handle_lorcast_command") as mock_handle,
        ):

            mock_parse.return_value = argparse.Namespace(command="lorcast")
            cli.run()

            mock_handle.assert_called_once()

    def test_run_with_no_command(self, cli):
        """Test running CLI with no command (shows help)."""
        with (
            patch.object(cli.parser, "parse_args") as mock_parse,
            patch.object(cli.parser, "print_help") as mock_help,
        ):

            mock_parse.return_value = argparse.Namespace(command=None)
            cli.run()

            mock_help.assert_called_once()


class TestMainFunction:
    """Test class for the main function."""

    @patch("inkcollector.cli.InkcollectorCLI")
    def test_main_success(self, mock_cli_class):
        """Test successful execution of main function."""
        mock_cli = Mock()
        mock_cli_class.return_value = mock_cli

        main()

        mock_cli_class.assert_called_once()
        mock_cli.run.assert_called_once()

    @patch("inkcollector.cli.InkcollectorCLI")
    def test_main_keyboard_interrupt(self, mock_cli_class):
        """Test main function handling of KeyboardInterrupt."""
        mock_cli = Mock()
        mock_cli.run.side_effect = KeyboardInterrupt()
        mock_cli_class.return_value = mock_cli

        with patch("builtins.print") as mock_print:
            main()

        mock_print.assert_called_once_with("\nOperation cancelled by user.")

    @patch("inkcollector.cli.InkcollectorCLI")
    def test_main_general_exception(self, mock_cli_class):
        """Test main function handling of general exceptions."""
        mock_cli = Mock()
        mock_cli.run.side_effect = Exception("Test error")
        mock_cli_class.return_value = mock_cli

        with patch("builtins.print") as mock_print:
            main()

        mock_print.assert_called_once_with("An unexpected error occurred: Test error")


class TestIntegration:
    """Integration tests for CLI functionality."""

    def test_full_argument_parsing_get_sets(self):
        """Test full argument parsing for get-sets command."""
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            cli = InkcollectorCLI()
            args = cli.parser.parse_args(
                ["lorcast", "get-sets", "--json", "--save-json"]
            )

            assert args.command == "lorcast"
            assert args.lorcast_command == "get-sets"
            assert args.json is True
            assert args.save_json is True

    def test_full_argument_parsing_get_cards(self):
        """Test full argument parsing for get-cards command."""
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            cli = InkcollectorCLI()
            args = cli.parser.parse_args(
                [
                    "lorcast",
                    "get-cards",
                    "--set-id",
                    "test-set",
                    "--json",
                    "--save-json",
                    "--get-images",
                    "large",
                ]
            )

            assert args.command == "lorcast"
            assert args.lorcast_command == "get-cards"
            assert args.set_id == "test-set"
            assert args.json is True
            assert args.save_json is True
            assert args.get_images == "large"

    @patch("inkcollector.cli.LorcastAPI")
    def test_end_to_end_get_sets_flow(self, mock_lorcast_class, temp_dir):
        """Test end-to-end flow for get-sets command."""
        # Setup mock
        mock_lorcast = Mock()
        mock_sets = [{"id": "set1", "name": "Test Set"}]
        mock_lorcast.get_sets.return_value = mock_sets
        mock_lorcast_class.return_value = mock_lorcast

        # Create CLI with temp directory
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            cli = InkcollectorCLI()
            cli.data_output_dir = temp_dir

        # Parse arguments and run command
        args = cli.parser.parse_args(["lorcast", "get-sets", "--save-json"])

        with patch("builtins.print"):
            cli.handle_lorcast_command(args)

        # Verify API was called
        mock_lorcast.get_sets.assert_called_once()

        # Check that directory structure would be created
        # expected_dir = os.path.join(temp_dir, cli.LORCAST_DATASOURCE_DIR)
        # We can't easily test file creation due to mocking, but we can verify the flow

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield temp_dir
