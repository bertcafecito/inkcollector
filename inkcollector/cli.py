import click

from inkcollector import __version__
from inkcollector.lorcast import Lorcast
from inkcollector.utils.output import output_json, output_csv

@click.group(invoke_without_command=True)
@click.option("-v", "--version", is_flag=True, help="Show Inkcollector version.")
@click.pass_context
def main(ctx, version):
    if version:
        click.echo(f"Inkcollector {__version__}")
        ctx.exit()  # Exit after showing the version if no subcommand is provided
    elif not ctx.invoked_subcommand:
        click.echo("No command provided. Use --help for usage information.")

@main.group(help="Collects data from the Lorecast API.")
def lorcast():
    pass

@lorcast.command(help="Collects a list of all card sets available in the Lorcana Trading Card Game, including both standard and promotional sets.")
@click.option("-fn", "--filename", type=str, is_flag=False, help="Provides a filename to save the collected data.")
def sets(filename):
    click.echo("Collecting sets")
    lorcast=Lorcast()
    sets=lorcast.get_sets()

    # Check if the sets list is empty
    if not sets:
        click.echo("No sets found.")
        return None

    # Check if the sets list is not empty
    if sets:
        click.echo(f"Found {len(sets)} sets.")

    file = lorcast.file_output(sets, filename)
    # Check if the file was saved successfully
    if not file:
        click.echo("Failed to save the file.")
        return None
    
    if file:
        click.echo(f"File saved successfully.")
        return None

    click.echo("Error Occurred while saving the file.")

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
    click.echo("Collecting sets")
    lorcast=Lorcast()
    sets=lorcast.get_sets()
    cards=list()

    if sets:
        click.echo(f"Found {len(sets)} sets.")

    for set in sets:
        setid = set["id"]
        setname = set["name"]
        click.echo(f"Collecting cards from set id of {setid}")
        data=lorcast.get_cards(setid)

        if data:
            click.echo(f"Found {len(cards)} cards.")
            cards.append(data)

    if output and output == "JSON":
        click.echo('Outputting in JSON format')
        output_json(sets, "sets.json")
        output_json(cards, "cards.json")
    
    if output and output == "CSV":
        click.echo('Outputting in CSV format')
        output_csv(sets, "sets.csv")
        output_csv(cards, "cards.csv")
    
    