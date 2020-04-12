"""Module to extrac Euromillions result."""
from datetime import date
from urllib.request import urlopen
from typing import (
    Optional,
    Tuple
)

import typer
from bs4 import BeautifulSoup


# Euromillions main URL for scrapy the results
EURO_MAIN_URL = "https://www.euro-millions.com/results/"


def get_euro_millions_result(draw_date: date) -> Optional[Tuple[int, ...]]:
    """Extract the result from a web page.

    Parameters
    ----------
    draw_date : date
        Euromillions draw date.

    Returns
    -------
    Optional[Tuple[int, ...]]
        Numbers drawn where the last two are the star numbers.
    """
    url = EURO_MAIN_URL + '{:%d-%m-%Y}'.format(draw_date)
    try:
        page = urlopen(url)
    except Exception as e:
        typer.echo(
            typer.style("ERROR: ", fg=typer.colors.RED, bold=True) +
            f"Unable do read web page with results [{str(e)}]."
        )
        return None

    soup = BeautifulSoup(page, 'html.parser')
    balls = soup.find('div', {'id': 'jsBallOrderCell'})
    if balls is None:
        typer.echo(
            typer.style("ERROR: ", fg=typer.colors.RED, bold=True) +
            f"Unable do find results on web page."
        )
        return None

    numbers = []
    stars = []
    for li in balls.findAll('li'):
        if li.attrs['class'][1] == 'ball':
            numbers.append(int(li.getText()))
        elif li.attrs['class'][1] == 'lucky-star':
            stars.append(int(li.getText()))

    return tuple(numbers) + tuple(stars)
