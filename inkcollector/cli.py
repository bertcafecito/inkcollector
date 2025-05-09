import click

from inkcollector import __version__
from inkcollector.lorcast import Lorcast
from inkcollector.utils.output import output_json, output_csv

@click.group()
@click.option("-v", "--version", is_flag=True, help="Show Inkcollector version.")
def main(version):
    if version:
        click.echo(f"Inkcollector {__version__}")

@main.group(help="Collects data from the Lorecast API.")
def lorcast():
    pass

@lorcast.command(help="Collects a list of all card sets available in the Lorcana Trading Card Game, including both standard and promotional sets.")
@click.option("-o", "--output", type=click.Choice(["JSON", "CSV"], case_sensitive=True), is_flag=False, help="Output format for the collected data.")
def sets(output):
    click.echo("Collecting sets")
    lorcast=Lorcast()
    sets=lorcast.get_sets()

    if sets:
        click.echo(f"Found {len(sets)} sets.")
    
    if output and output == "JSON":
        click.echo("Outputting in JSON format")
        output_json(sets, "sets.json")
    
    if output and output == "CSV":
        click.echo("Outputting in CSV format")
        output_csv(sets, "sets.csv")

@lorcast.command(help="Collects a detailed information about a specific Lorcana card set by using either the set's code or its unique identifier (ID).")
@click.option("--setid", type=str, help="Provide a set's code or its unique identifier (ID).")
@click.option("-o", "--output", type=click.Choice(["JSON", "CSV"], case_sensitive=True), is_flag=False, help="Output format for the collected data.")
def cards(setid, output):
    click.echo(f"Collecting cards from set id of {setid}")
    lorcast=Lorcast()
    cards=lorcast.get_cards(setid)

    if cards:
        click.echo(f"Found {len(cards)} cards.")

    if output and output == "JSON":
        click.echo('Outputting in JSON format')
        output_json(cards, "cards.json")
    
    if output and output == "CSV":
        click.echo('Outputting in CSV format')
        output_csv(cards, "cards.csv")

@lorcast.command(help="Collects everything.")
@click.option("-o", "--output", type=click.Choice(["JSON", "CSV"], case_sensitive=True), is_flag=False, help="Output format for the collected data.")
def all(output):
    click.echo('Collecting everthing')

    if output and output == "JSON":
        click.echo('Outputting in JSON format')
    
    if output and output == "CSV":
        click.echo('Outputting in CSV format')
    
    