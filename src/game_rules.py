"""Module with rules to generate a game."""

import numpy as np


def already_happen(game: np.ndarray, games: np.ndarray) -> bool:
    """Check if a game exists in a list of games.

    Parameters
    ----------
    game : np.ndarray
        Game to be checked.
    games : np.ndarray
        List of existing games.

    Returns
    -------
    bool
        True if the given game exists in the list, otherwise False.
    """
    return next((True for g in games if all(g == game)), False)


def has_only_even(game: np.ndarray) -> bool:
    """Check if a game has only even numbers.

    Parameters
    ----------
    game : np.ndarray
        Game to be checked.

    Returns
    -------
    bool
        True if the game has only even number, otherwise False.
    """
    return all(map(lambda x: x % 2 != 0, game))


def has_only_odd(game: np.ndarray) -> bool:
    """Check if a game has only odd numbers.

    Parameters
    ----------
    game : np.ndarray
        Game to be checked.

    Returns
    -------
    bool
        True if the game has only odd number, otherwise False.
    """
    return all(map(lambda x: x % 2 == 0, game))
