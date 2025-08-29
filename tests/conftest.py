"""
Test fixtures and conftest for inkcollector tests.

This module provides common fixtures and configuration for all tests.
"""

import tempfile
from unittest.mock import Mock

import pytest

from inkcollector.lorcast import LorcastAPI


@pytest.fixture
def temp_directory():
    """Create a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def mock_lorcast_api():
    """Create a mock LorcastAPI instance with common return values."""
    mock_api = Mock(spec=LorcastAPI)

    # Default return values for multiple sets
    mock_api.get_sets.return_value = [
        {"id": "set1", "name": "First Set", "released_at": "2023-01-01"},
        {"id": "set2", "name": "Second Set", "released_at": "2023-06-01"},
        {"id": "set3", "name": "Third Set", "released_at": "2023-12-01"},
    ]

    mock_api.get_set.return_value = {
        "id": "set1",
        "name": "First Set",
        "released_at": "2023-01-01",
    }

    # Mock cards with different counts per set for testing
    def mock_get_cards(set_id):
        if set_id == "set1":
            return [
                {
                    "id": "card1",
                    "name": "Test Card 1",
                    "set_id": "set1",
                    "image_uris": {
                        "digital": {
                            "small": "http://example.com/card1_small.jpg",
                            "normal": "http://example.com/card1_normal.jpg",
                            "large": "http://example.com/card1_large.jpg",
                        }
                    },
                },
                {
                    "id": "card2",
                    "name": "Test Card 2",
                    "set_id": "set1",
                    "image_uris": {
                        "digital": {
                            "small": "http://example.com/card2_small.jpg",
                            "normal": "http://example.com/card2_normal.jpg",
                            "large": "http://example.com/card2_large.jpg",
                        }
                    },
                },
            ]
        elif set_id == "set2":
            return [
                {
                    "id": "card3",
                    "name": "Test Card 3",
                    "set_id": "set2",
                    "image_uris": {
                        "digital": {
                            "small": "http://example.com/card3_small.jpg",
                            "normal": "http://example.com/card3_normal.jpg",
                            "large": "http://example.com/card3_large.jpg",
                        }
                    },
                },
            ]
        elif set_id == "set3":
            return [
                {
                    "id": "card4",
                    "name": "Test Card 4",
                    "set_id": "set3",
                    "image_uris": {
                        "digital": {
                            "small": "http://example.com/card4_small.jpg",
                            "normal": "http://example.com/card4_normal.jpg",
                            "large": "http://example.com/card4_large.jpg",
                        }
                    },
                },
                {
                    "id": "card5",
                    "name": "Test Card 5",
                    "set_id": "set3",
                    "image_uris": {
                        "digital": {
                            "small": "http://example.com/card5_small.jpg",
                            "normal": "http://example.com/card5_normal.jpg",
                            "large": "http://example.com/card5_large.jpg",
                        }
                    },
                },
                {
                    "id": "card6",
                    "name": "Test Card 6",
                    "set_id": "set3",
                    "image_uris": {
                        "digital": {
                            "small": "http://example.com/card6_small.jpg",
                            "normal": "http://example.com/card6_normal.jpg",
                            "large": "http://example.com/card6_large.jpg",
                        }
                    },
                },
            ]
        else:
            return []

    mock_api.get_cards.side_effect = mock_get_cards

    return mock_api


@pytest.fixture
def sample_sets_data():
    """Sample sets data for testing."""
    return [
        {
            "id": "TFC",
            "name": "The First Chapter",
            "released_at": "2023-08-18",
            "code": "TFC",
            "card_count": 204,
        },
        {
            "id": "ROF",
            "name": "Rise of the Floodborn",
            "released_at": "2023-11-17",
            "code": "ROF",
            "card_count": 204,
        },
    ]


@pytest.fixture
def sample_cards_data():
    """Sample cards data for testing."""
    return [
        {
            "id": "1",
            "name": "Mickey Mouse - Brave Little Tailor",
            "set_id": "TFC",
            "rarity": "Legendary",
            "cost": 8,
            "image_uris": {
                "digital": {
                    "small": "http://example.com/1_small.jpg",
                    "normal": "http://example.com/1_normal.jpg",
                    "large": "http://example.com/1_large.jpg",
                }
            },
        },
        {
            "id": "2",
            "name": "Elsa - Snow Queen",
            "set_id": "TFC",
            "rarity": "Super Rare",
            "cost": 6,
            "image_uris": {
                "digital": {
                    "small": "http://example.com/2_small.jpg",
                    "normal": "http://example.com/2_normal.jpg",
                    "large": "http://example.com/2_large.jpg",
                }
            },
        },
    ]


@pytest.fixture
def cli_args_sets_json():
    """Command line arguments for sets with JSON output."""
    from argparse import Namespace

    return Namespace(
        command="lorcast", lorcast_command="get-sets", json=True, save_json=False
    )


@pytest.fixture
def cli_args_sets_save():
    """Command line arguments for sets with save to file."""
    from argparse import Namespace

    return Namespace(
        command="lorcast", lorcast_command="get-sets", json=False, save_json=True
    )


@pytest.fixture
def cli_args_cards_with_images():
    """Command line arguments for cards with image download."""
    from argparse import Namespace

    return Namespace(
        command="lorcast",
        lorcast_command="get-cards",
        set_id="TFC",
        json=True,
        save_json=True,
        get_images="large",
    )


@pytest.fixture
def cli_args_cards_no_images():
    """Command line arguments for cards without image download."""
    from argparse import Namespace

    return Namespace(
        command="lorcast",
        lorcast_command="get-cards",
        set_id="TFC",
        json=False,
        save_json=False,
        get_images=None,
    )


@pytest.fixture
def cli_args_get_all_sets_basic():
    """Command line arguments for get-all-sets with basic options."""
    from argparse import Namespace

    return Namespace(
        command="lorcast",
        lorcast_command="get-all-sets",
        json=False,
        save_json=True,
        get_images=None,
    )


@pytest.fixture
def cli_args_get_all_sets_with_json():
    """Command line arguments for get-all-sets with JSON output."""
    from argparse import Namespace

    return Namespace(
        command="lorcast",
        lorcast_command="get-all-sets",
        json=True,
        save_json=True,
        get_images=None,
    )


@pytest.fixture
def cli_args_get_all_sets_with_images():
    """Command line arguments for get-all-sets with image download."""
    from argparse import Namespace

    return Namespace(
        command="lorcast",
        lorcast_command="get-all-sets",
        json=False,
        save_json=True,
        get_images="normal",
    )
