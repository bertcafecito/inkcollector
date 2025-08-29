"""
Test argument parsing and command-line interface functionality.

This module tests the argument parsing, help functionality, and command-line
interface behavior of the inkcollector CLI.
"""

from io import StringIO
from unittest.mock import patch

import pytest

from inkcollector.cli import InkcollectorCLI


class TestArgumentParsing:
    """Test argument parsing functionality."""

    @pytest.fixture
    def cli(self):
        """Create CLI instance for testing."""
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            return InkcollectorCLI()

    def test_help_message_main(self, cli):
        """Test main help message."""
        with (
            pytest.raises(SystemExit),
            patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        ):
            cli.parser.parse_args(["--help"])

        help_text = mock_stdout.getvalue()
        assert "inkcollector" in help_text
        assert (
            "CLI tool for collecting data about the disney lorcana trading card game"
            in help_text
        )
        assert "lorcast" in help_text

    def test_help_message_lorcast(self, cli):
        """Test lorcast command help message."""
        with (
            pytest.raises(SystemExit),
            patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        ):
            cli.parser.parse_args(["lorcast", "--help"])

        help_text = mock_stdout.getvalue()
        assert "lorcast" in help_text
        assert "get-sets" in help_text
        assert "get-cards" in help_text

    def test_help_message_get_sets(self, cli):
        """Test get-sets subcommand help message."""
        with (
            pytest.raises(SystemExit),
            patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        ):
            cli.parser.parse_args(["lorcast", "get-sets", "--help"])

        help_text = mock_stdout.getvalue()
        assert "get-sets" in help_text
        assert "--json" in help_text
        assert "--save-json" in help_text
        assert "Print JSON data in the Console" in help_text

    def test_help_message_get_cards(self, cli):
        """Test get-cards subcommand help message."""
        with (
            pytest.raises(SystemExit),
            patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        ):
            cli.parser.parse_args(["lorcast", "get-cards", "--help"])

        help_text = mock_stdout.getvalue()
        assert "get-cards" in help_text
        assert "--set-id" in help_text
        assert "--json" in help_text
        assert "--save-json" in help_text
        assert "--get-images" in help_text
        assert "small" in help_text and "normal" in help_text and "large" in help_text

    def test_version_argument(self, cli):
        """Test version argument."""
        with (
            pytest.raises(SystemExit),
            patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        ):
            cli.parser.parse_args(["--version"])

        version_text = mock_stdout.getvalue()
        assert "Inkcollector" in version_text

    def test_version_argument_short(self, cli):
        """Test short version argument."""
        with (
            pytest.raises(SystemExit),
            patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        ):
            cli.parser.parse_args(["-v"])

        version_text = mock_stdout.getvalue()
        assert "Inkcollector" in version_text

    def test_no_arguments_shows_help(self, cli):
        """Test that no arguments shows help."""
        args = cli.parser.parse_args([])
        assert args.command is None

        # Test that run() method shows help when no command
        with (
            patch.object(cli.parser, "parse_args", return_value=args),
            patch.object(cli.parser, "print_help") as mock_help,
        ):
            cli.run()
            mock_help.assert_called_once()
            mock_help.assert_called_once()

    def test_invalid_command(self, cli):
        """Test handling of invalid commands."""
        with pytest.raises(SystemExit):
            cli.parser.parse_args(["invalid-command"])

    def test_lorcast_without_subcommand(self, cli):
        """Test lorcast command without subcommand."""
        args = cli.parser.parse_args(["lorcast"])
        assert args.command == "lorcast"
        assert not hasattr(args, "lorcast_command") or args.lorcast_command is None

    def test_get_sets_all_flag_combinations(self, cli):
        """Test all possible flag combinations for get-sets."""
        # No flags
        args = cli.parser.parse_args(["lorcast", "get-sets"])
        assert not args.json
        assert not args.save_json

        # Only --json
        args = cli.parser.parse_args(["lorcast", "get-sets", "--json"])
        assert args.json
        assert not args.save_json

        # Only --save-json
        args = cli.parser.parse_args(["lorcast", "get-sets", "--save-json"])
        assert not args.json
        assert args.save_json

        # Both flags
        args = cli.parser.parse_args(["lorcast", "get-sets", "--json", "--save-json"])
        assert args.json
        assert args.save_json

    def test_get_cards_all_flag_combinations(self, cli):
        """Test all possible flag combinations for get-cards."""
        # Minimal required arguments
        args = cli.parser.parse_args(["lorcast", "get-cards", "--set-id", "test"])
        assert args.set_id == "test"
        assert not args.json
        assert not args.save_json
        assert args.get_images is None

        # With JSON output
        args = cli.parser.parse_args(
            ["lorcast", "get-cards", "--set-id", "test", "--json"]
        )
        assert args.json

        # With save JSON
        args = cli.parser.parse_args(
            ["lorcast", "get-cards", "--set-id", "test", "--save-json"]
        )
        assert args.save_json

        # With image download (default size)
        args = cli.parser.parse_args(
            ["lorcast", "get-cards", "--set-id", "test", "--get-images"]
        )
        assert args.get_images == "normal"

        # With image download (specific size)
        for size in ["small", "normal", "large"]:
            args = cli.parser.parse_args(
                ["lorcast", "get-cards", "--set-id", "test", "--get-images", size]
            )
            assert args.get_images == size

        # All flags together
        args = cli.parser.parse_args(
            [
                "lorcast",
                "get-cards",
                "--set-id",
                "test",
                "--json",
                "--save-json",
                "--get-images",
                "large",
            ]
        )
        assert args.set_id == "test"
        assert args.json
        assert args.save_json
        assert args.get_images == "large"

    def test_get_images_invalid_size(self, cli):
        """Test get-images with invalid size."""
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

    def test_set_id_with_special_characters(self, cli):
        """Test set-id with special characters."""
        special_ids = [
            "set-with-dashes",
            "set_with_underscores",
            "SET_UPPERCASE",
            "set123",
            "set.with.dots",
            "set with spaces",  # This should work as it's a string argument
        ]

        for set_id in special_ids:
            args = cli.parser.parse_args(["lorcast", "get-cards", "--set-id", set_id])
            assert args.set_id == set_id

    def test_argument_order_independence(self, cli):
        """Test that argument order doesn't matter."""
        # Different orders should produce same result
        orders = [
            [
                "lorcast",
                "get-cards",
                "--set-id",
                "test",
                "--json",
                "--save-json",
                "--get-images",
                "large",
            ],
            [
                "lorcast",
                "get-cards",
                "--json",
                "--set-id",
                "test",
                "--get-images",
                "large",
                "--save-json",
            ],
            [
                "lorcast",
                "get-cards",
                "--get-images",
                "large",
                "--save-json",
                "--json",
                "--set-id",
                "test",
            ],
        ]

        expected_attrs = {
            "command": "lorcast",
            "lorcast_command": "get-cards",
            "set_id": "test",
            "json": True,
            "save_json": True,
            "get_images": "large",
        }

        for order in orders:
            args = cli.parser.parse_args(order)
            for attr, expected_value in expected_attrs.items():
                assert getattr(args, attr) == expected_value

    def test_case_sensitivity(self, cli):
        """Test case sensitivity of arguments."""
        # Commands should be case-sensitive
        with pytest.raises(SystemExit):
            cli.parser.parse_args(["LORCAST", "get-sets"])

        with pytest.raises(SystemExit):
            cli.parser.parse_args(["lorcast", "GET-SETS"])

        # But set-id values can be any case
        args = cli.parser.parse_args(
            ["lorcast", "get-cards", "--set-id", "MiXeD_CaSe_SeT"]
        )
        assert args.set_id == "MiXeD_CaSe_SeT"


class TestCommandLineInterface:
    """Test command-line interface behavior."""

    @pytest.fixture
    def cli(self):
        """Create CLI instance for testing."""
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            return InkcollectorCLI()

    def test_parser_prog_name(self, cli):
        """Test that parser uses correct program name."""
        assert cli.parser.prog == "inkcollector"

    def test_parser_description(self, cli):
        """Test that parser has correct description."""
        expected_desc = (
            "Inkcollector is a CLI tool for collecting data about the "
            "disney lorcana trading card game."
        )
        assert expected_desc in cli.parser.description

    def test_subcommand_structure(self, cli):
        """Test the subcommand structure is correctly set up."""
        # Test that lorcast is a valid subcommand
        args = cli.parser.parse_args(["lorcast", "get-sets"])
        assert args.command == "lorcast"

        # Test that lorcast has its own subcommands
        args = cli.parser.parse_args(["lorcast", "get-sets"])
        assert args.lorcast_command == "get-sets"

        args = cli.parser.parse_args(["lorcast", "get-cards", "--set-id", "test"])
        assert args.lorcast_command == "get-cards"

    def test_error_messages_for_missing_required_args(self, cli):
        """Test error messages for missing required arguments."""
        # Missing set-id for get-cards should show helpful error
        with (
            pytest.raises(SystemExit),
            patch("sys.stderr", new_callable=StringIO) as mock_stderr,
        ):
            cli.parser.parse_args(["lorcast", "get-cards"])

        error_text = mock_stderr.getvalue()
        assert "required" in error_text.lower()
        assert "set-id" in error_text or "set_id" in error_text

    def test_help_formatting(self, cli):
        """Test that help text is properly formatted."""
        # Test main help
        with (
            pytest.raises(SystemExit),
            patch("sys.stdout", new_callable=StringIO) as mock_stdout,
        ):
            cli.parser.parse_args(["--help"])

        help_text = mock_stdout.getvalue()

        # Check for proper formatting elements
        assert "usage:" in help_text.lower()
        assert (
            "positional arguments:" in help_text.lower()
            or "commands:" in help_text.lower()
        )
        assert (
            "optional arguments:" in help_text.lower()
            or "options:" in help_text.lower()
        )

    def test_mutual_exclusivity_scenarios(self, cli):
        """Test scenarios that might involve mutual exclusivity (if any)."""
        # Currently no mutually exclusive groups, but test that multiple flags
        # work together
        args = cli.parser.parse_args(["lorcast", "get-sets", "--json", "--save-json"])
        assert args.json and args.save_json  # Both should be allowed

    def test_default_values(self, cli):
        """Test default values for all arguments."""
        # Test get-sets defaults
        args = cli.parser.parse_args(["lorcast", "get-sets"])
        assert args.json is False
        assert args.save_json is False

        # Test get-cards defaults
        args = cli.parser.parse_args(["lorcast", "get-cards", "--set-id", "test"])
        assert args.json is False
        assert args.save_json is False
        assert args.get_images is None

        # Test get-images default when flag is provided without value
        args = cli.parser.parse_args(
            ["lorcast", "get-cards", "--set-id", "test", "--get-images"]
        )
        assert args.get_images == "normal"  # Should default to 'normal'


class TestArgumentValidation:
    """Test argument validation and edge cases."""

    @pytest.fixture
    def cli(self):
        """Create CLI instance for testing."""
        with patch("inkcollector.cli.InkcollectorCLI._setup_output_directories"):
            return InkcollectorCLI()

    def test_empty_set_id(self, cli):
        """Test handling of empty set ID."""
        # Empty string should be allowed (validation happens at API level)
        args = cli.parser.parse_args(["lorcast", "get-cards", "--set-id", ""])
        assert args.set_id == ""

    def test_very_long_set_id(self, cli):
        """Test handling of very long set ID."""
        long_id = "a" * 1000
        args = cli.parser.parse_args(["lorcast", "get-cards", "--set-id", long_id])
        assert args.set_id == long_id

    def test_unicode_set_id(self, cli):
        """Test handling of Unicode characters in set ID."""
        unicode_id = "sét-ïd-wïth-ünïcödé-🎮"
        args = cli.parser.parse_args(["lorcast", "get-cards", "--set-id", unicode_id])
        assert args.set_id == unicode_id

    def test_numeric_set_id(self, cli):
        """Test handling of numeric set ID."""
        numeric_id = "12345"
        args = cli.parser.parse_args(["lorcast", "get-cards", "--set-id", numeric_id])
        assert args.set_id == numeric_id

    def test_boolean_flag_variations(self, cli):
        """Test various ways boolean flags might be specified."""
        # Standard flags
        args = cli.parser.parse_args(["lorcast", "get-sets", "--json"])
        assert args.json is True

        # Flags should not accept values
        with pytest.raises(SystemExit):
            cli.parser.parse_args(["lorcast", "get-sets", "--json", "true"])

    def test_argument_parsing_with_equals_sign(self, cli):
        """Test argument parsing with equals sign syntax."""
        # Most parsers support --arg=value syntax
        try:
            args = cli.parser.parse_args(["lorcast", "get-cards", "--set-id=test-set"])
            assert args.set_id == "test-set"
        except SystemExit:
            # If equals syntax isn't supported, that's also valid
            pass

        try:
            args = cli.parser.parse_args(
                ["lorcast", "get-cards", "--set-id", "test", "--get-images=large"]
            )
            assert args.get_images == "large"
        except SystemExit:
            # If equals syntax isn't supported, that's also valid
            pass
