"""Functions to deal with database."""
import csv
import pathlib
import sqlite3

from contextlib import contextmanager
from datetime import date
from typing import (
    Optional,
    Tuple
)

import typer

DBFILE = pathlib.Path("database.db")

CREATE_EURO_RESULTS_TABLE = """
    CREATE TABLE euro_results (
        dt date NOT NULL PRIMARY KEY,
        n1 int NOT NULL,
        n2 int NOT NULL,
        n3 int NOT NULL,
        n4 int NOT NULL,
        n5 int NOT NULL,
        s1 int NOT NULL,
        s2 int NOT NULL
    )
"""

CREATE_EURO_LAST_DRAW_TABLE = """
    CREATE TABLE last_draw (
        dt date NOT NULL
    )
"""


@contextmanager
def connect():
    """Yield a SQLite3 connection.

    With a context manager will, automatically, close the connection.
    """
    try:
        connection = sqlite3.connect(
            DBFILE,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        connection.row_factory = sqlite3.Row
        yield connection
    finally:
        connection.close()


def delete_database():
    """Delete the existing database file."""
    if DBFILE.exists():
        DBFILE.unlink()


def init_database() -> bool:
    """Initialize a new, empty, database file.

    Returns
    -------
    bool
        If database already exists it will return False.
    """
    if DBFILE.exists():
        return False

    create_tables()
    return True


def export_database(filename: str) -> bool:
    """Export the results table to CSV file.

    Parameters
    ----------
    filename : str
        File name and path to the CSV file.

    Returns
    -------
    bool
        Returns True if the CSV file was generated.
    """
    if not DBFILE.exists():
        return False

    fn = pathlib.Path(filename)

    with connect() as con:
        rows = con.execute("SELECT * FROM euro_results").fetchall()

    if rows is None:
        return False

    with open(fn, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow([key for key in rows[0].keys()])
        csv_writer.writerows(rows)

    return True


def create_tables():
    """Create the tables for a new database."""
    with connect() as con:
        con.execute(CREATE_EURO_RESULTS_TABLE)
        con.execute(CREATE_EURO_LAST_DRAW_TABLE)


def update_last_draw_date():
    """Update the last draw date.

    The last draw date will be highest date value on the results table.
    """
    with connect() as con:
        row = con.execute("SELECT MAX(dt) AS last FROM euro_results").fetchone()
        if row:
            con.execute("DELETE FROM last_draw")
            con.execute("INSERT INTO last_draw VALUES(?)", (row['last'], ))
            con.commit()


def get_last_draw_date() -> Optional[date]:
    """Get the last draw date stored.

    Returns
    -------
    Optional[date]
        The date of tha last draw. Returns None if there is no date.
    """
    with connect() as con:
        row = con.execute("SELECT dt FROM last_draw").fetchone()
        dt = row['dt'] if row else None

    return dt


def get_result_by_date(dt: date) -> Optional[Tuple[int, ...]]:
    """Get the result for a given date.

    Parameters
    ----------
    dt : date
        Date when the draw happened.

    Returns
    -------
    Optional[Tuple[int, ...]]
        Number from the draw where the last two are the stars.
        Returns None if the date didn't exists on the table.
    """
    query = f"SELECT n1, n2, n3, n4, n5, s1, s2 FROM euro_results where dt = ?"

    with connect() as con:
        row = con.execute(query, (dt,)).fetchone()

    return tuple(row) if row else None


def get_number_of_results() -> int:
    """Get the total of results stored.

    Returns
    -------
    int
        Number of results stored on the database.
    """
    query = "SELECT count(1) AS n from euro_results"

    with connect() as con:
        row = con.execute(query).fetchone()

    return row['n']


def insert_new_result(draw_date: date, result: Tuple[int, ...]) -> bool:
    """Insert a new Euromillions results into the database.

    Parameters
    ----------
    draw_date : date
        Date of the draw.
    result : Tuple[List[int], List[int]]
        Number from the draw where the last two are the stars.

    Returns
    -------
    bool
        Return True if insert was successful, False otherwise.
    """
    query = f"INSERT INTO euro_results VALUES({','.join('?' * 8)})"

    try:
        with connect() as con:
            con.execute(query, (draw_date, ) + result)
            con.commit()
    except sqlite3.IntegrityError:
        typer.echo(
            typer.style("ERROR: ", fg=typer.colors.RED, bold=True) +
            f"Unable save result on database [this date was already collected]."
        )
        return False
    except Exception as e:
        typer.echo(
            typer.style("ERROR: ", fg=typer.colors.RED, bold=True) +
            f"Unable save result on database [{str(e)}]."
        )
        return False

    update_last_draw_date()

    return True
