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
        return sets

    click.echo("Error Occurred while saving the file.")

@lorcast.command(help="Collects a detailed information about a specific Lorcana card set by using either the set's code or its unique identifier (ID).")
@click.option("--setid", required=True, type=str, help="Provide a set's code or its unique identifier (ID).")
@click.option("-fn", "--filename", type=str, is_flag=False, help="Provides a filename to save the collected data.")
def cards(setid, filename):
    click.echo(f"Collecting cards from set id of {setid}")
    lorcast=Lorcast()
    cards=lorcast.get_cards(setid)

    # Check if the cards list is empty
    if not cards:
        click.echo("No cards found.")
        return None

    # Check if the cards list is not empty
    if cards:
        click.echo(f"Found {len(cards)} cards.")

    file = lorcast.file_output(cards, filename)
    # Check if the file was saved successfully
    if not file:
        click.echo("Failed to save the file.")
        return None
    
    if file:
        click.echo(f"File saved successfully.")
        return None
    
    click.echo("Error Occurred while saving the file.")

@lorcast.command(help="Collects everything.")
@click.option("-of", "--outputformat", required=True, type=click.Choice(["JSON"], case_sensitive=False), is_flag=False, help="Output format for the collected data.")
@click.pass_context
def all(ctx, outputformat):
    click.echo('Collecting everthing')

    if outputformat:
        file_ext = outputformat.lower()
        sets_filename = f"lorcast/sets.{file_ext}"

        # Invoke the 'sets' command
        sets_data = ctx.invoke(sets, filename=sets_filename)

        # Invoke the 'cards' command for each set
        for set_data in sets_data:
            set_id = set_data["id"]
            set_name = set_data["name"]
            cards_filename = f"lorcast/sets/{set_name}.{file_ext}"
            ctx.invoke(cards, setid=set_id, filename=cards_filename)

    