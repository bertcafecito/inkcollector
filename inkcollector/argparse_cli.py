import argparse

from inkcollector import __version__


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
    
    # Parse arguments
    args = parser.parse_args()


if __name__ == '__main__':
    main()
