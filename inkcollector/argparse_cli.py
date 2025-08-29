import argparse

from inkcollector import __version__


class InkcollectorCLI:
    """Class-based CLI for Inkcollector application."""
    
    def __init__(self):
        """Initialize the CLI parser."""
        self.parser = None
        self._setup_parser()
    
    def _setup_parser(self):
        """Set up the argument parser and subcommands."""
        self.parser = argparse.ArgumentParser(
            prog='inkcollector',
            description='Inkcollector is a CLI tool for collecting data about the disney lorcana trading card game.',
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Add version argument
        self.parser.add_argument(
            '-v', '--version',
            action='version',
            version=f'Inkcollector {__version__}'
        )
        
        # Create subparsers for commands
        subparsers = self.parser.add_subparsers(dest='command', help='Available commands')
        
        # Add lorcast command
        self._setup_lorcast_parser(subparsers)
    
    def _setup_lorcast_parser(self, subparsers):
        """Set up the lorcast command parser and its subcommands."""
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
    
    def handle_lorcast_command(self, args):
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
    
    def run(self):
        """Parse arguments and execute the appropriate command."""
        args = self.parser.parse_args()
        
        # Handle commands
        if args.command == 'lorcast':
            self.handle_lorcast_command(args)


def main():
    """Main entry point for the argparse-based CLI."""
    cli = InkcollectorCLI()
    cli.run()


if __name__ == '__main__':
    main()
