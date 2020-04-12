"""Module to generate a games."""
from enum import Enum
from typing import (
    List,
    Optional,
    Tuple
)

import numpy as np
import pandas as pd

from game_rules import (
    already_happen,
    has_only_even,
    has_only_odd
)
from sqlite import connect


NUMBER_COLS = ['n1', 'n2', 'n3', 'n4', 'n5']
STAR_COLS = ['s1', 's2']

K_NUMBERS = 5
K_STARS = 2


class GameType(str, Enum):
    """Class of type of games."""

    random = "random"
    high_frequency = "high_frequency"
    low_frequency = "low_frequency"


def get_games_and_stats() -> Tuple[np.ndarray, ...]:
    """Retrieve all games stored and calculate main statistics.

    Returns
    -------
    Tuple[np.ndarray, ...]
        The function returns:
        - An array with all games stored into the database

        - An array with all unique numbers
        - An array with the normal probability of each number (Higher the frequency -> Higher the probability)
        - An array with the inverse probability of each number (Lower the frequency -> Higher the probability)

        - An array with all unique stars
        - An array with the normal probability of each star (Higher the frequency -> Higher the probability)
        - An array with the inverse probability of each star (Lower the frequency -> Higher the probability)

    """
    with connect() as con:
        data = pd.read_sql('select * from euro_results', con, parse_dates=['dt'])

    games = data.loc[:, NUMBER_COLS + STAR_COLS].values

    numbers, number_counts = np.unique(data.loc[:, NUMBER_COLS], return_counts=True)
    stars, star_counts = np.unique(data.loc[:, STAR_COLS], return_counts=True)

    # Higher the frequency - Higher the probability
    number_probs = number_counts / number_counts.sum()
    star_probs = star_counts / star_counts.sum()

    # Lower the frequency - Higher the probability
    number_inv_probs = (1 / number_counts) / (1 / number_counts).sum()
    star_inv_probs = (1 / star_counts) / (1 / star_counts).sum()

    return games, numbers, number_probs, number_inv_probs, stars, star_probs, star_inv_probs


def choose_numbers(values: np.ndarray, k: int, probability: Optional[np.ndarray] = None) -> np.ndarray:
    """Choose k number from an array considering a given probability.

    Parameters
    ----------
    values : np.ndarray
        List of all possible values to be chosen.
    k : int
        Number of values to be chosen.
    probability : Optional[np.ndarray], optional
        The probability to be chosen for each value, by default None (all values have the same probability).

    Returns
    -------
    np.ndarray
        An array with the chosen values.
    """
    return np.sort(np.random.choice(values, k, replace=False, p=probability))


def gen_game_weighted(
    numbers: np.ndarray,
    stars: np.ndarray,
    numbers_prob: Optional[np.ndarray] = None,
    stars_prob: Optional[np.ndarray] = None
) -> np.ndarray:
    """Generate a game based on probabilities.

    Parameters
    ----------
    numbers : np.ndarray
        An array of number values to be chosen.
    stars : np.ndarray
        An array of star values to be chosen.
    numbers_prob : Optional[np.ndarray], optional
        An array of probabilities for each number value, by default None.
    stars_prob : Optional[np.ndarray], optional
        An array of probabilities for each star value, by default None.

    Returns
    -------
    np.ndarray
        A game where the last two values are stars.
    """
    return np.concatenate((
        choose_numbers(numbers, K_NUMBERS, numbers_prob),
        choose_numbers(stars, K_STARS, stars_prob)
    ))


def generate_multiple_games(game_types: List[GameType], number_of_games: int) -> List[Tuple[GameType, np.ndarray]]:
    """Generate multiple games based on type.

    Parameters
    ----------
    game_types : List[GameType]
        List of game types to be generated.
    number_of_games : int
        Number of games to generate for each game type.

    Returns
    -------
    List[Tuple[GameType, np.ndarray]]
        List of games generated grouped by type.
    """
    games_drawn, nums, p_nums, pinv_nums, stars, p_stars, pinv_stars = get_games_and_stats()

    generated_games_by_type: List[Tuple[GameType, np.ndarray]] = []
    all_games_generated: List[np.ndarray] = []

    for gt in game_types:
        ng = 0
        game_lst = []
        while ng < number_of_games:
            game = {
                GameType.random: gen_game_weighted(nums, stars),
                GameType.high_frequency: gen_game_weighted(nums, stars, p_nums, p_stars),
                GameType.low_frequency: gen_game_weighted(nums, stars, pinv_nums, pinv_stars)
            }[gt]

            # Check the rules
            if has_only_even(game[:K_NUMBERS]):
                continue
            if has_only_odd(game[:K_NUMBERS]):
                continue
            if already_happen(game, games_drawn):
                continue
            if already_happen(game, all_games_generated):
                continue

            # Add game to list if pass all rules
            game_lst.append(game)
            all_games_generated.append(game)
            ng = ng + 1

        generated_games_by_type.append((gt, game_lst))

    return generated_games_by_type
