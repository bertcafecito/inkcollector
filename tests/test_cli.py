import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from inkcollector.cli import sets, cards, all

# filepath: /workspaces/inkcollector/inkcollector/test_cli.py

@pytest.fixture
def runner():
    return CliRunner()

@patch("inkcollector.cli.Lorcast")
def test_sets_command(mock_lorcast, runner):
    # Mock Lorcast behavior
    mock_instance = MagicMock()
    mock_lorcast.return_value = mock_instance
    mock_instance.get_sets.return_value = [{"id": "1", "name": "Set1"}]
    mock_instance.file_output.return_value = True

    # Run the command
    result = runner.invoke(sets, ["--filename", "output.json"])

    # Assertions
    assert result.exit_code == 0
    assert "Found 1 sets." in result.output
    assert "File saved successfully." in result.output
    mock_instance.get_sets.assert_called_once()
    mock_instance.file_output.assert_called_once_with([{"id": "1", "name": "Set1"}], "output.json")

@patch("inkcollector.cli.Lorcast")
def test_cards_command(mock_lorcast, runner):
    # Mock Lorcast behavior
    mock_instance = MagicMock()
    mock_lorcast.return_value = mock_instance
    mock_instance.get_cards.return_value = [{"id": "101", "name": "Card1"}]
    mock_instance.file_output.return_value = True

    # Run the command
    result = runner.invoke(cards, ["--setid", "1", "--filename", "cards.json"])

    # Assertions
    assert result.exit_code == 0
    assert "Found 1 cards." in result.output
    assert "File saved successfully." in result.output
    mock_instance.get_cards.assert_called_once_with("1")
    mock_instance.file_output.assert_called_once_with([{"id": "101", "name": "Card1"}], "cards.json")

@patch("inkcollector.cli.Lorcast")
def test_all_command(mock_lorcast, runner):
    # Mock Lorcast behavior
    mock_instance = MagicMock()
    mock_lorcast.return_value = mock_instance
    mock_instance.get_sets.return_value = [{"id": "1", "name": "Set1"}]
    mock_instance.get_cards.return_value = [{"id": "101", "name": "Card1"}]
    mock_instance.file_output.return_value = True

    # Run the command
    result = runner.invoke(all, ["--outputformat", "JSON"])

    # Assertions
    assert result.exit_code == 0
    assert "Collecting everthing" in result.output
    assert "Found 1 sets." in result.output
    assert "Found 1 cards." in result.output
    assert "File saved successfully." in result.output
    mock_instance.get_sets.assert_called_once()
    mock_instance.get_cards.assert_called_once_with("1")
    mock_instance.file_output.assert_any_call([{"id": "1", "name": "Set1"}], "lorcast/sets.json")
    mock_instance.file_output.assert_any_call([{"id": "101", "name": "Card1"}], "lorcast/sets/Set1.json")