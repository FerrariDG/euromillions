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

from game_generator import K_NUMBERS


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


def format_numbers(nums: Tuple) -> str:
    """Format an array of numbers.

    Parameters
    ----------
    lst : Tuple
        Array with numbers to be formatted

    Returns
    -------
    str
        String with number formatted

    Example
    -------
    >>> format_numbers((2, 3, 10, 15))
    ' 2,  3, 10, 15'
    """
    return ', '.join(map(lambda x: f"{x:2d}", nums))


def print_game(result: Tuple[int, ...]):
    """Print the Euromillions game.

    Parameters
    ----------
    result : Tuple[int, ...]
        Tuple with the seven numbers where the last two are the stars.
    """
    typer.echo(
        "\tNumbers: " +
        typer.style(format_numbers(result[:K_NUMBERS]), fg=typer.colors.GREEN) +
        "\tStars  : " +
        typer.style(format_numbers(result[K_NUMBERS:]), fg=typer.colors.GREEN)
    )
