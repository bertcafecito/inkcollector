import click

from inkcollector import __version__

@click.command()
@click.option("-v", "--version", is_flag=True, help="Show Inkcollector version.")
def main(version):
    if version:
        click.echo(f"Inkcollector {__version__}")