"""General helper functions."""
from datetime import (
    datetime,
    timedelta
)
from typing import (
    Iterator,
    Tuple
)

import typer


def days_between(start: datetime, end: datetime) -> Iterator[Tuple[int, datetime]]:
    """Yield all days between to dates including the start and end date.

    Parameters
    ----------
    start : datetime
        Initial date for the yield loop.
    end : datetime
        Final date for the yield loop.

    Yields
    ------
    Iterator[Tuple[int, datetime]]
        It yields a tuple with the index, relative to the start date,
        and the current date on the loop.
    """
    for idx, i in enumerate(range(0, (end - start).days)):
        yield (idx, start + timedelta(days=i))


def print_result(result: Tuple[int, ...]):
    """Print the Euromillions results.

    Parameters
    ----------
    result : Tuple[int, ...]
        Tuple with the seven numbers where the last two are the stars.
    """
    typer.echo(
        "\tNumbers: " +
        typer.style(f"{', '.join(map(str,result[:5]))}", fg=typer.colors.GREEN)
    )
    typer.echo(
        "\tStars  : " +
        typer.style(f"{', '.join(map(str,result[5:]))}", fg=typer.colors.GREEN)
    )
