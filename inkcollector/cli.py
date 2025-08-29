import argparse
import json
import os
from typing import Any, Dict, List, Optional

import yaml

from inkcollector import __version__
from inkcollector.config import (
    ConfigManager,
    ExtractionProfile,
    InkcollectorConfig,
)
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
        self.config_manager = ConfigManager()
        self.config: InkcollectorConfig = self.config_manager.load_config()

        # Use workspace config for output directories
        workspace = self.config.get_workspace(self.config.default_workspace)
        if workspace:
            self.data_output_dir = workspace.data_output_dir
            self.image_output_dir = workspace.image_output_dir
        else:
            self.data_output_dir = self.DATA_OUTPUT_DIR
            self.image_output_dir = self.IMAGE_OUTPUT_DIR

        # Track if custom directories were specified via command line
        self.using_custom_data_dir = False
        self.using_custom_image_dir = False

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

        # Add global arguments
        self.parser.add_argument(
            "--config", type=str, help="Path to configuration file"
        )
        self.parser.add_argument("--workspace", type=str, help="Workspace name to use")
        self.parser.add_argument(
            "--profile", type=str, help="Extraction profile to use"
        )

        # Create subparsers for commands
        subparsers = self.parser.add_subparsers(
            dest="command", help="Available commands"
        )

        # Add config command
        self._setup_config_parser(subparsers)

        # Add lorcast command
        self._setup_lorcast_parser(subparsers)

    def _setup_config_parser(self, subparsers: argparse._SubParsersAction) -> None:
        """Set up the config command parser and its subcommands."""
        config_parser = subparsers.add_parser(
            "config", help="Configuration management commands"
        )

        # Add subcommands for config
        config_subparsers = config_parser.add_subparsers(
            dest="config_command", help="Configuration subcommands"
        )

        # Add init subcommand
        init_parser = config_subparsers.add_parser(
            "init", help="Create a sample configuration file"
        )
        init_parser.add_argument(
            "--path",
            type=str,
            default=".inkcollector.yaml",
            help="Path for the configuration file (default: .inkcollector.yaml)",
        )
        init_parser.add_argument(
            "--force", action="store_true", help="Overwrite existing configuration file"
        )

        # Add show subcommand
        show_parser = config_subparsers.add_parser(
            "show", help="Show current configuration"
        )
        show_parser.add_argument(
            "--format",
            choices=["yaml", "json"],
            default="yaml",
            help="Output format (default: yaml)",
        )

        # Add list subcommand
        list_parser = config_subparsers.add_parser(
            "list", help="List available profiles and workspaces"
        )
        list_parser.add_argument(
            "--profiles", action="store_true", help="List available profiles"
        )
        list_parser.add_argument(
            "--workspaces", action="store_true", help="List available workspaces"
        )

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
        get_sets_parser.add_argument(
            "--output-dir", type=str, help="Custom base directory for data storage"
        )
        get_sets_parser.add_argument(
            "--image-dir", type=str, help="Custom base directory for image storage"
        )

        # Add get-cards subcommand
        get_cards_parser = lorcast_subparsers.add_parser(
            "get-cards", help="Get cards data"
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
        get_cards_parser.add_argument(
            "--output-dir", type=str, help="Custom base directory for data storage"
        )
        get_cards_parser.add_argument(
            "--image-dir", type=str, help="Custom base directory for image storage"
        )

        # Add get-all-sets subcommand
        get_all_sets_parser = lorcast_subparsers.add_parser(
            "get-all-sets", help="Get all sets and their cards in a single operation"
        )
        get_all_sets_parser.add_argument(
            "--json", action="store_true", help="Print JSON data in the Console"
        )
        get_all_sets_parser.add_argument(
            "--save-json", action="store_true", help="Save JSON data to a file"
        )
        get_all_sets_parser.add_argument(
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
        get_all_sets_parser.add_argument(
            "--output-dir", type=str, help="Custom base directory for data storage"
        )
        get_all_sets_parser.add_argument(
            "--image-dir", type=str, help="Custom base directory for image storage"
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

        # Apply workspace and profile overrides
        self._apply_args_overrides(args)

        # Apply directory overrides if specified
        self._apply_directory_overrides(args)

        lorcast = LorcastAPI()

        if args.lorcast_command == "get-sets":
            self._handle_get_sets_command(lorcast, args)
        elif args.lorcast_command == "get-cards":
            self._handle_get_cards_command(lorcast, args)
        elif args.lorcast_command == "get-all-sets":
            self._handle_get_all_sets_command(lorcast, args)
        else:
            print(f"Unknown lorcast subcommand: {args.lorcast_command}")

    def handle_config_command(self, args: argparse.Namespace) -> None:
        """Handle config command and route to appropriate subcommand handler.

        Args:
            args: Parsed command line arguments
        """
        if not hasattr(args, "config_command") or not args.config_command:
            print("Use --help to see available config subcommands.")
            return

        if args.config_command == "init":
            self._handle_config_init_command(args)
        elif args.config_command == "show":
            self._handle_config_show_command(args)
        elif args.config_command == "list":
            self._handle_config_list_command(args)
        else:
            print(f"Unknown config subcommand: {args.config_command}")

    def _apply_args_overrides(self, args: argparse.Namespace) -> None:
        """Apply command line overrides for workspace and profile.

        Args:
            args: Parsed command line arguments
        """
        # This method is kept for backward compatibility
        # Global overrides are now handled in _apply_global_overrides
        pass

    def _apply_directory_overrides(self, args: argparse.Namespace) -> None:
        """Apply command line directory overrides.

        Args:
            args: Parsed command line arguments
        """
        # Override data output directory if specified
        if hasattr(args, "output_dir") and args.output_dir:
            self.data_output_dir = args.output_dir
            self.using_custom_data_dir = True
            self._create_directory_if_not_exists(self.data_output_dir)
            print(f"Using custom data output directory: {self.data_output_dir}")

        # Override image output directory if specified
        if hasattr(args, "image_dir") and args.image_dir:
            self.image_output_dir = args.image_dir
            self.using_custom_image_dir = True
            self._create_directory_if_not_exists(self.image_output_dir)
            print(f"Using custom image output directory: {self.image_output_dir}")

    def _handle_config_init_command(self, args: argparse.Namespace) -> None:
        """Handle the config init subcommand.

        Args:
            args: Parsed command line arguments
        """
        config_path = args.path

        if os.path.exists(config_path) and not args.force:
            print(f"Configuration file already exists at {config_path}")
            print("Use --force to overwrite")
            return

        try:
            self.config_manager.create_sample_config(config_path)
            print(f"Sample configuration file created at {config_path}")
        except Exception as e:
            print(f"Error creating configuration file: {e}")

    def _handle_config_show_command(self, args: argparse.Namespace) -> None:
        """Handle the config show subcommand.

        Args:
            args: Parsed command line arguments
        """
        if args.format == "json":
            config_dict = self.config_manager._config_to_dict(self.config)
            print(json.dumps(config_dict, indent=2))
        else:  # yaml
            config_dict = self.config_manager._config_to_dict(self.config)
            print(
                yaml.dump(
                    config_dict, default_flow_style=False, sort_keys=False, indent=2
                )
            )

    def _handle_config_list_command(self, args: argparse.Namespace) -> None:
        """Handle the config list subcommand.

        Args:
            args: Parsed command line arguments
        """
        if args.profiles or (not args.profiles and not args.workspaces):
            print("Available Profiles:")
            for name, profile in self.config.profiles.items():
                print(f"  {name}: {profile.description}")
            print()

        if args.workspaces or (not args.profiles and not args.workspaces):
            print("Available Workspaces:")
            for name, workspace in self.config.workspaces.items():
                print(
                    f"  {name}: data='{workspace.data_output_dir}', "
                    f"images='{workspace.image_output_dir}', "
                    f"profile='{workspace.default_profile}'"
                )

    def _get_effective_profile(self, args: argparse.Namespace) -> ExtractionProfile:
        """Get the effective extraction profile based on args and config.

        Args:
            args: Parsed command line arguments

        Returns:
            ExtractionProfile to use for the operation
        """
        # Use profile from command line if specified
        if hasattr(args, "profile") and args.profile:
            profile = self.config.get_profile(args.profile)
            if profile:
                return profile
            else:
                print(f"Warning: Profile '{args.profile}' not found, using default")

        # Use workspace default profile
        workspace_name = getattr(args, "workspace", self.config.default_workspace)
        workspace = self.config.get_workspace(workspace_name)
        if workspace:
            profile = self.config.get_profile(workspace.default_profile)
            if profile:
                return profile

        # Fallback to complete profile
        return self.config.get_profile("complete") or self.config.profiles["complete"]

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

        # Get effective profile settings
        profile = self._get_effective_profile(args)

        # Apply profile settings, with command line overrides
        should_print = (
            args.json if hasattr(args, "json") and args.json else profile.print_json
        )
        should_save = (
            args.save_json
            if hasattr(args, "save_json") and args.save_json
            else (profile.save_json and profile.extract_data)
        )

        if should_print:
            self._print_sets_json(sets)

        if should_save:
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

        # Get effective profile settings
        profile = self._get_effective_profile(args)

        # Apply profile settings, with command line overrides
        should_print = (
            args.json if hasattr(args, "json") and args.json else profile.print_json
        )
        should_save = (
            args.save_json
            if hasattr(args, "save_json") and args.save_json
            else (profile.save_json and profile.extract_data)
        )
        should_download_images = args.get_images is not None or (
            profile.extract_images and not hasattr(args, "get_images")
        )

        # Determine image size
        if hasattr(args, "get_images") and args.get_images:
            image_size = args.get_images
        elif profile.extract_images:
            image_size = profile.image_size
        else:
            image_size = "normal"

        if should_print:
            self._print_cards_json(cards, set_id)

        if should_save:
            self._save_cards_to_file(cards, set_id)

        if should_download_images:
            self._download_card_images(lorcast, cards, set_id, image_size)

    def _handle_get_all_sets_command(
        self, lorcast: LorcastAPI, args: argparse.Namespace
    ) -> None:
        """Handle the get-all-sets subcommand.

        Args:
            lorcast: LorcastAPI instance
            args: Parsed command line arguments
        """
        print("Fetching all sets and their cards...")

        # First, get all sets
        sets = lorcast.get_sets()

        if not sets:
            print("No sets found.")
            return

        print(f"Found {len(sets)} sets.")

        # Get effective profile settings
        profile = self._get_effective_profile(args)

        # Apply profile settings, with command line overrides
        should_print = (
            args.json if hasattr(args, "json") and args.json else profile.print_json
        )
        should_save = (
            args.save_json
            if hasattr(args, "save_json") and args.save_json
            else (profile.save_json and profile.extract_data)
        )
        should_download_images = (
            hasattr(args, "get_images") and args.get_images is not None
        ) or (profile.extract_images and not hasattr(args, "get_images"))

        # Determine image size
        if hasattr(args, "get_images") and args.get_images:
            image_size = args.get_images
        elif profile.extract_images:
            image_size = profile.image_size
        else:
            image_size = "normal"

        # Save sets data if requested
        if should_save:
            self._save_sets_to_file(sets)

        # Print sets data if requested
        if should_print:
            self._print_sets_json(sets)

        # Process each set to get cards
        total_cards = 0
        successful_image_downloads = 0

        for i, set_data in enumerate(sets, 1):
            set_id = set_data.get("id")
            set_name = set_data.get("name", "Unknown")

            if not set_id:
                print(f"Set {i} has no ID, skipping...")
                continue

            print(f"\nProcessing set {i}/{len(sets)}: {set_name} (ID: {set_id})")

            try:
                # Get cards for this set
                cards = lorcast.get_cards(set_id)

                if not cards:
                    print(f"No cards found for set {set_id}")
                    continue

                print(f"Found {len(cards)} cards for set {set_id}")
                total_cards += len(cards)

                # Print cards data if requested
                if should_print:
                    self._print_cards_json(cards, set_id)

                # Save cards data if requested
                if should_save:
                    self._save_cards_to_file(cards, set_id)

                # Download images if requested
                if should_download_images:
                    print(f"Downloading images for set {set_id}...")
                    set_successful_downloads = self._download_card_images_bulk(
                        lorcast, cards, set_id, image_size
                    )
                    successful_image_downloads += set_successful_downloads

            except Exception as e:
                print(f"Error processing set {set_id}: {e}")
                continue

        print(f"\n{'=' * 60}")
        print(f"{'BULK EXTRACTION COMPLETE':^60}")
        print(f"{'=' * 60}")
        print(f"Processed {len(sets)} sets")
        print(f"Total cards extracted: {total_cards}")

        if should_download_images:
            print(f"Total images downloaded: {successful_image_downloads}")

    def _download_card_images_bulk(
        self,
        lorcast: LorcastAPI,
        cards: List[Dict[str, Any]],
        set_id: str,
        image_size: str = "normal",
    ) -> int:
        """Download images for all cards in a set (bulk version with progress).

        Args:
            lorcast: LorcastAPI instance
            cards: List of card data dictionaries
            set_id: ID of the set
            image_size: Size of the image to download ('small', 'normal', 'large')

        Returns:
            Number of successful downloads
        """
        if self.using_custom_image_dir:
            # Full override: save directly to custom directory without subdirectories
            output_path = self.image_output_dir
        else:
            # Default behavior: use lorcast subdirectory structure
            output_path = os.path.join(
                self.image_output_dir, self.LORCAST_DATASOURCE_DIR, "sets", set_id
            )
            self._create_directory_if_not_exists(output_path)

        successful_downloads = 0

        for i, card in enumerate(cards, 1):
            print(f"  Downloading image {i}/{len(cards)}...", end=" ")
            if self._download_single_card_image(lorcast, card, output_path, image_size):
                successful_downloads += 1
                print("✓")
            else:
                print("✗")

        print(f"  Successfully downloaded {successful_downloads}/{len(cards)} images")
        return successful_downloads

    def _print_sets_json(self, sets: List[Dict[str, Any]]) -> None:
        """Print sets data as formatted JSON.

        Args:
            sets: List of set data dictionaries
        """
        print(f"\n{'=' * 60}")
        print(f"{'DISNEY LORCANA SETS':^60}")
        print(f"{'=' * 60}")
        print(f"Found {len(sets)} sets:\n")
        print(json.dumps(sets, indent=2))

    def _print_cards_json(self, cards: List[Dict[str, Any]], set_id: str) -> None:
        """Print cards data as formatted JSON.

        Args:
            cards: List of card data dictionaries
            set_id: ID of the set
        """
        print(f"\n{'=' * 60}")
        print(f"{'DISNEY LORCANA CARDS':^60}")
        print(f"{'=' * 60}")
        print(f"Found {len(cards)} cards in set {set_id}:\n")
        print(json.dumps(cards, indent=2))

    def _save_sets_to_file(self, sets: List[Dict[str, Any]]) -> None:
        """Save sets data to a JSON file.

        Args:
            sets: List of set data dictionaries
        """
        if self.using_custom_data_dir:
            # Full override: save directly to custom directory without subdirectories
            output_path = self.data_output_dir
            file_path = os.path.join(output_path, "sets.json")
        else:
            # Default behavior: use lorcast subdirectory
            output_path = os.path.join(
                self.data_output_dir, self.LORCAST_DATASOURCE_DIR
            )
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
        if self.using_custom_data_dir:
            # Full override: save directly to custom directory with set filename
            output_path = self.data_output_dir
            file_path = os.path.join(output_path, f"{set_id}.json")
        else:
            # Default behavior: use lorcast subdirectory structure
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
        if self.using_custom_image_dir:
            # Full override: save directly to custom directory without subdirectories
            output_path = self.image_output_dir
        else:
            # Default behavior: use lorcast subdirectory structure
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

        # Apply global overrides before executing commands
        self._apply_global_overrides(args)

        # Handle commands
        if args.command == "lorcast":
            self.handle_lorcast_command(args)
        elif args.command == "config":
            self.handle_config_command(args)
        else:
            # If no command is provided, show help
            self.parser.print_help()

    def _apply_global_overrides(self, args: argparse.Namespace) -> None:
        """Apply global overrides like config file, workspace, etc.

        Args:
            args: Parsed command line arguments
        """
        # Override config file if specified
        if hasattr(args, "config") and args.config:
            self.config = self.config_manager.load_config(args.config)
            # Update workspace settings after config reload
            workspace = self.config.get_workspace(self.config.default_workspace)
            if workspace:
                self.data_output_dir = workspace.data_output_dir
                self.image_output_dir = workspace.image_output_dir
                self._setup_output_directories()

        # Override workspace if specified
        if hasattr(args, "workspace") and args.workspace:
            workspace = self.config.get_workspace(args.workspace)
            if workspace:
                self.data_output_dir = workspace.data_output_dir
                self.image_output_dir = workspace.image_output_dir
                self._setup_output_directories()
            else:
                print(
                    f"Warning: Workspace '{args.workspace}' not found in configuration"
                )


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
