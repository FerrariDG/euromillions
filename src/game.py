"""Module with client commands to generate new games."""
from typing import (
    List
)

import typer

from game_generator import (
    GameType,
    generate_multiple_games
)
from utils import print_game


def generate_games(
    game_types: List[GameType] = typer.Option(
        None, "--type", "-t", show_choices=True,
        help="Game type. It can be multiple types at once."
    ),
    number_of_games: int = typer.Option(
        1, "--num-of-games", "-n", show_default=True,
        help="Number of games generate for each type."
    )
):
    """Generate multiple games for each game type passed."""
    if not game_types:
        game_types = [GameType.random, GameType.high_frequency, GameType.low_frequency]

    games = generate_multiple_games(game_types, number_of_games)

    for gt, lst in games:
        typer.echo("Games of type " + typer.style(gt.value, fg=typer.colors.GREEN, bold=True))
        for g in lst:
            print_game(g)


if __name__ == "__main__":
    app = typer.Typer(add_completion=False)
    app.command()(generate_games)
    app()
