import argparse
import json
import os
from typing import Any, Dict, List, Optional

from inkcollector import __version__
from inkcollector.lorcast import LorcastAPI


class InkcollectorCLI:
    """Class-based CLI for Inkcollector application.

    This CLI provides commands for collecting Disney Lorcana trading card data
    through various APIs and data sources.
    """

    # Constants
    DATA_OUTPUT_DIR = "data"
    IMAGE_OUTPUT_DIR = "images"
    LORCAST_DATASOURCE_DIR = "lorcast"

    def __init__(self):
        """Initialize the CLI parser and setup directories."""
        self.parser: Optional[argparse.ArgumentParser] = None
        self.data_output_dir = self.DATA_OUTPUT_DIR
        self.image_output_dir = self.IMAGE_OUTPUT_DIR

        self._setup_output_directories()
        self._setup_parser()

    def _setup_output_directories(self) -> None:
        """Create output directories for data and images if they don't exist."""
        self._create_directory_if_not_exists(self.data_output_dir)
        self._create_directory_if_not_exists(self.image_output_dir)

    def _create_directory_if_not_exists(self, directory: str) -> None:
        """Create a directory if it doesn't exist.

        Args:
            directory: Path to the directory to create
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

    def _setup_parser(self) -> None:
        """Set up the argument parser and subcommands."""
        self.parser = argparse.ArgumentParser(
            prog="inkcollector",
            description=(
                "Inkcollector is a CLI tool for collecting data about the "
                "disney lorcana trading card game."
            ),
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        # Add version argument
        self.parser.add_argument(
            "-v", "--version", action="version", version=f"Inkcollector {__version__}"
        )

        # Create subparsers for commands
        subparsers = self.parser.add_subparsers(
            dest="command", help="Available commands"
        )

        # Add lorcast command
        self._setup_lorcast_parser(subparsers)

    def _setup_lorcast_parser(self, subparsers: argparse._SubParsersAction) -> None:
        """Set up the lorcast command parser and its subcommands."""
        lorcast_parser = subparsers.add_parser(
            "lorcast", help="Lorcast command (under development)"
        )

        # Add subcommands for lorcast
        lorcast_subparsers = lorcast_parser.add_subparsers(
            dest="lorcast_command", help="Lorcast subcommands"
        )

        # Add get-sets subcommand
        get_sets_parser = lorcast_subparsers.add_parser(
            "get-sets", help="Get sets data"
        )
        get_sets_parser.add_argument(
            "--json", action="store_true", help="Print JSON data in the Console"
        )
        get_sets_parser.add_argument(
            "--save-json", action="store_true", help="Save JSON data to a file"
        )

        # Add get-cards subcommand
        get_cards_parser = lorcast_subparsers.add_parser(
            "get-cards", help="Get cards data (under development)"
        )
        get_cards_parser.add_argument(
            "--set-id", type=str, required=True, help="ID of the set to get cards from"
        )
        get_cards_parser.add_argument(
            "--json", action="store_true", help="Print JSON data in the Console"
        )
        get_cards_parser.add_argument(
            "--save-json", action="store_true", help="Save JSON data to a file"
        )
        get_cards_parser.add_argument(
            "--get-images",
            nargs="?",
            choices=["small", "normal", "large"],
            const="normal",
            default=None,
            help=(
                "Download card images with specified size "
                "(choices: small, normal, large; default: normal)"
            ),
        )

    def handle_lorcast_command(self, args: argparse.Namespace) -> None:
        """Handle lorcast command and route to appropriate subcommand handler.

        Args:
            args: Parsed command line arguments
        """
        if not hasattr(args, "lorcast_command") or not args.lorcast_command:
            print(
                "Lorcast command is under development. "
                "Use --help to see available subcommands."
            )
            return

        lorcast = LorcastAPI()

        if args.lorcast_command == "get-sets":
            self._handle_get_sets_command(lorcast, args)
        elif args.lorcast_command == "get-cards":
            self._handle_get_cards_command(lorcast, args)
        else:
            print(f"Unknown lorcast subcommand: {args.lorcast_command}")

    def _handle_get_sets_command(
        self, lorcast: LorcastAPI, args: argparse.Namespace
    ) -> None:
        """Handle the get-sets subcommand.

        Args:
            lorcast: LorcastAPI instance
            args: Parsed command line arguments
        """
        print("Fetching sets data...")
        sets = lorcast.get_sets()

        if not sets:
            print("No sets found.")
            return

        print(f"Found {len(sets)} sets.")

        if args.json:
            self._print_sets_json(sets)

        if args.save_json:
            self._save_sets_to_file(sets)

    def _handle_get_cards_command(
        self, lorcast: LorcastAPI, args: argparse.Namespace
    ) -> None:
        """Handle the get-cards subcommand.

        Args:
            lorcast: LorcastAPI instance
            args: Parsed command line arguments
        """
        set_id = args.set_id
        print(f"Fetching cards data for set {set_id}...")
        set = lorcast.get_set(set_id)
        set_id = set.get("id", None)
        if not set_id:
            print(f"Set with id {args.set_id} not found.")
            return
        cards = lorcast.get_cards(set_id)

        print(f"Found {len(cards)} cards for set id {set_id}.")

        if args.json:
            self._print_cards_json(cards, set_id)

        if args.save_json:
            self._save_cards_to_file(cards, set_id)

        if args.get_images:
            self._download_card_images(lorcast, cards, set_id, args.get_images)

    def _print_sets_json(self, sets: List[Dict[str, Any]]) -> None:
        """Print sets data as formatted JSON.

        Args:
            sets: List of set data dictionaries
        """
        print(f"\n{'='*60}")
        print(f"{'DISNEY LORCANA SETS':^60}")
        print(f"{'='*60}")
        print(f"Found {len(sets)} sets:\n")
        print(json.dumps(sets, indent=2))

    def _print_cards_json(self, cards: List[Dict[str, Any]], set_id: str) -> None:
        """Print cards data as formatted JSON.

        Args:
            cards: List of card data dictionaries
            set_id: ID of the set
        """
        print(f"\n{'='*60}")
        print(f"{'DISNEY LORCANA CARDS':^60}")
        print(f"{'='*60}")
        print(f"Found {len(cards)} cards in set {set_id}:\n")
        print(json.dumps(cards, indent=2))

    def _save_sets_to_file(self, sets: List[Dict[str, Any]]) -> None:
        """Save sets data to a JSON file.

        Args:
            sets: List of set data dictionaries
        """
        output_path = os.path.join(self.data_output_dir, self.LORCAST_DATASOURCE_DIR)
        self._create_directory_if_not_exists(output_path)

        file_path = os.path.join(output_path, "sets.json")

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(sets, f, ensure_ascii=False, indent=2)
            print(f"Sets data saved to {file_path}")
        except Exception as e:
            print(f"Error saving sets data to {file_path}: {e}")

    def _save_cards_to_file(self, cards: List[Dict[str, Any]], set_id: str) -> None:
        """Save cards data to a JSON file.

        Args:
            cards: List of card data dictionaries
            set_id: ID of the set
        """
        output_path = os.path.join(
            self.data_output_dir, self.LORCAST_DATASOURCE_DIR, "sets"
        )
        self._create_directory_if_not_exists(output_path)

        file_path = os.path.join(output_path, f"{set_id}.json")

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(cards, f, ensure_ascii=False, indent=2)
            print(f"Cards data saved to {file_path}")
        except Exception as e:
            print(f"Error saving cards data to {file_path}: {e}")

    def _download_card_images(
        self,
        lorcast: LorcastAPI,
        cards: List[Dict[str, Any]],
        set_id: str,
        image_size: str = "normal",
    ) -> None:
        """Download images for all cards in a set.

        Args:
            lorcast: LorcastAPI instance
            cards: List of card data dictionaries
            set_id: ID of the set
            image_size: Size of the image to download ('small', 'normal', 'large')
        """
        output_path = os.path.join(
            self.image_output_dir, self.LORCAST_DATASOURCE_DIR, "sets", set_id
        )
        self._create_directory_if_not_exists(output_path)

        print(f"Downloading images for {len(cards)} cards...")
        successful_downloads = 0

        for card in cards:
            if self._download_single_card_image(lorcast, card, output_path, image_size):
                successful_downloads += 1

        print(
            f"Successfully downloaded {successful_downloads} out of "
            f"{len(cards)} card images."
        )

    def _download_single_card_image(
        self,
        lorcast: LorcastAPI,
        card: Dict[str, Any],
        output_path: str,
        image_size: str = "normal",
    ) -> bool:
        """Download image for a single card.

        Args:
            lorcast: LorcastAPI instance
            card: Card data dictionary
            output_path: Directory to save the image
            image_size: Size of the image to download ('small', 'normal', 'large')

        Returns:
            True if download was successful, False otherwise
        """
        card_id = card.get("id")
        if not card_id:
            print("Card ID not found, skipping image download.")
            return False

        image_uris = card.get("image_uris")
        if not image_uris:
            print(
                f"No image URIs found for card {card_id}, " "skipping image download."
            )
            return False

        # Navigate through the nested structure safely
        digital_uris = image_uris.get("digital")
        if not digital_uris:
            print(
                f"No digital image URIs found for card {card_id}, "
                "skipping image download."
            )
            return False

        image_uri = digital_uris.get(image_size)
        if not image_uri:
            print(
                f"No {image_size} image URI found for card {card_id}, "
                "skipping image download."
            )
            return False

        try:
            image_output_path = os.path.join(output_path, f"crd_{card_id}.jpg")
            lorcast.download_image(image_uri, image_output_path)
            return True
        except Exception as e:
            print(f"Error downloading image for card {card_id}: {e}")
            return False

    def run(self) -> None:
        """Parse arguments and execute the appropriate command."""
        args = self.parser.parse_args()

        # Handle commands
        if args.command == "lorcast":
            self.handle_lorcast_command(args)
        else:
            # If no command is provided, show help
            self.parser.print_help()


def main() -> None:
    """Main entry point for the argparse-based CLI."""
    try:
        cli = InkcollectorCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
