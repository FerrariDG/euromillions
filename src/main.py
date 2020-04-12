"""Module with client commands to the database."""
from datetime import (
    datetime,
    timedelta
)

import typer

from database import (
    delete_database,
    export_database,
    get_number_of_results,
    get_last_draw_date,
    get_result_by_date,
    init_database,
    insert_new_result
)

from scrapper import (
    get_euro_millions_result
)

from utils import (
    days_between,
    print_result
)


app = typer.Typer(add_completion=False)


@app.command(name='init')
def initialize(overwrite: bool = typer.Option(False, help='Overwrite existing database.', show_default=True)):
    """
    Initialize database.

    If --overwrite is used, the existing database will be deleted.
    """
    if overwrite:
        delete = typer.confirm("Are you sure you want to delete the existing database?")
        if not delete:
            raise typer.Abort()

        delete_database()
        typer.echo("Current database deleted.")

    if init_database():
        typer.echo("New database created.")
    else:
        typer.echo("Database file already exists.")


@app.command(name='status')
def database_status():
    """
    Show the database current status.

    Number of results stored |
    Last draw date stored |
    Last results stored.
    """
    last_draw_date = get_last_draw_date()
    result = get_result_by_date(last_draw_date)
    total = get_number_of_results()

    typer.echo(
        "Results stored: " +
        typer.style(str(total), fg=typer.colors.GREEN, bold=True)
    )

    typer.echo(
        "Last draw date: " +
        typer.style(f"{last_draw_date}", fg=typer.colors.GREEN, bold=True)
    )

    typer.echo("Last result:")
    if result:
        print_result(result)
    else:
        typer.secho("\tNo result found", fg=typer.colors.YELLOW)


@app.command(name='update')
def update_result(
    draw_date: datetime = typer.Option(
        default="2004-02-13",
        formats=["%Y-%m-%d"],
        help="Date to get Euromillions draw numbers.",
        show_default=True
    )
):
    """
    Update Euromillions result for a given date.

    If --draw_date is not passed, it will update with the date of the first Euromillions result.
    """
    typer.echo(
        "Getting results for: " +
        typer.style(f"{draw_date:%Y-%m-%d}", fg=typer.colors.GREEN, bold=True)
    )

    result = get_euro_millions_result(draw_date.date())

    if result:
        if insert_new_result(draw_date.date(), result):
            typer.echo("Result saved!")
            print_result(result)


@app.command(name='full-update')
def full_update(
    max_days: int = typer.Option(
        default=None,
        help="Runs the update for a maximun number of days"
    )
):
    """Update Euromillions results from last date stored until today."""
    start = datetime(2004, 2, 13)
    current_date = datetime.today()

    last_date = get_last_draw_date()
    if last_date:
        start = datetime(last_date.year, last_date.month, last_date.day) + timedelta(days=1)

    for idx, dt in days_between(start, current_date):
        typer.echo(f"Processing day {idx+1}")
        update_result(dt)
        if max_days and idx + 1 == max_days:
            break

    typer.echo("Update process finished.")


@app.command(name='export')
def export_database_to_csv(filename: str = typer.Option(
    default="euromillions.csv",
    help="CSV filename, it can be an absolute path."
)):
    """Export all results on the database to a CSV file."""
    export_database(filename)
    typer.echo("Database exported.")


if __name__ == "__main__":
    app()
