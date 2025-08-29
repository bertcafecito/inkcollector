import argparse

from inkcollector import __version__


def handle_lorcast_command(args):
    """Handle lorcast command and its subcommands."""
    if hasattr(args, 'lorcast_command') and args.lorcast_command:
        if args.lorcast_command == 'get-sets':
            print("Get-sets option is under development")
        elif args.lorcast_command == 'get-cards':
            print("Get-cards option is under development")
        elif args.lorcast_command == 'get-images':
            print("Get-images option is under development")
    else:
        print("Lorcast command is under development. Use --help to see available subcommands.")


def main():
    """Main entry point for the argparse-based CLI."""
    parser = argparse.ArgumentParser(
        prog='inkcollector',
        description='Inkcollector is a CLI tool for collecting data about the disney lorcana trading card game.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Add version argument
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'Inkcollector {__version__}'
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add lorcast command
    lorcast_parser = subparsers.add_parser(
        'lorcast',
        help='Lorcast command (under development)'
    )
    
    # Add subcommands for lorcast
    lorcast_subparsers = lorcast_parser.add_subparsers(dest='lorcast_command', help='Lorcast subcommands')
    
    # Add get-sets subcommand
    get_sets_parser = lorcast_subparsers.add_parser(
        'get-sets',
        help='Get sets data (under development)'
    )
    
    # Add get-cards subcommand
    get_cards_parser = lorcast_subparsers.add_parser(
        'get-cards',
        help='Get cards data (under development)'
    )
    
    # Add get-images subcommand
    get_images_parser = lorcast_subparsers.add_parser(
        'get-images',
        help='Get images data (under development)'
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == 'lorcast':
        handle_lorcast_command(args)


if __name__ == '__main__':
    main()
