"""Module to extrac Euromillions result."""
from datetime import date
from urllib.request import urlopen
from typing import (
    Any,
    Dict,
    Optional
)

import numpy as np
import pandas as pd
import typer
from bs4 import BeautifulSoup


# Euromillions main URL for scrapy the results
EURO_MAIN_URL = "https://www.euro-millions.com/results/"


def get_euro_millions_result(draw_date: date) -> Optional[Dict[str, Any]]:
    """Extract the result from a web page.

    Parameters
    ----------
    draw_date : date
        Euromillions draw date.

    Returns
    -------
    Optional[Dict[str, Any]]
        Numbers drawn where the last two are the star numbers.
        Number of winners and main prize value.
    """
    url = EURO_MAIN_URL + '{:%d-%m-%Y}'.format(draw_date)
    try:
        page = urlopen(url)
    except Exception as e:
        typer.echo(
            typer.style("ERROR: ", fg=typer.colors.RED, bold=True) +
            f"Unable do read web page with results [{repr(e)}]."
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

    prizes = soup.find('table', {'class': "table breakdown mobFormat"})
    if prizes is None:
        typer.echo(
            typer.style("WARNING: ", fg=typer.colors.YELLOW, bold=True) +
            f"Unable do find prize and winners on web page."
        )
        return {'draw': tuple(numbers) + tuple(stars)}

    try:
        df = pd.read_html(str(prizes), flavor='bs4')[0]

        main_prize = int(float(df.iloc[0][1][1:].replace(',', '')))
        winners = 0 if type(df.iloc[0][4]) != np.int64 else int(df.iloc[0][4])
    except Exception as e:
        typer.echo(
            typer.style("WARNING: ", fg=typer.colors.YELLOW, bold=True) +
            f"Unable do find prize and winners on web page [{repr(e)}]."
        )
        return {'draw': tuple(numbers) + tuple(stars)}

    return {
        'draw': tuple(numbers) + tuple(stars),
        'winners': winners,
        'prize': main_prize
    }
