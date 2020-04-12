# EuroMillions Numbers Generator

This application get Euromillions results from internet and store on a local database file and use it to generate new numbers to gamble.

---

**NOTE**: There is <span style="color:red">**NO**</span> guarantee that you will win if you use the numbers generated to gamble at Euromillions, but I wish all the luck in the world.

---

## Topics

1. [Installation](#installation)
1. [Usage Instructions](#usage-instructions)
1. [Rules to Generate Games](#rules-to-generate-games)
1. [Managing the Database](#managing-the-database)

---

## Installation

To use this application you need to have installed Python 3.7+ and `pipenv`.

To install Python 3.7+ please visit the [Python website](https://www.python.org/).

To install `pipenv` please visit the [Pipenv website](https://pipenv-fork.readthedocs.io/en/latest/install.html#installing-pipenv). Usually the command below works very well.

```bash
pip3 install --user pipenv
```

To install the application dependencies run the command bellow inside the application folder.

```bash
pipenv sync
```

---

## Usage Instructions

With the application exists a database file but there is no guarantee that will be up-to-date.

To check the current database status run: `pipenv run database status`.

To make sure that all the Euromillions results are stored run: `pipenv run database full-update`.

For more instructions to manage the database [click here](#managing-the-database).

To generate on game for each game type just run: `pipenv run game`. For more info about game types and rules, [click here](#rules-to-generate-games).

```text
$ pipenv run game --help
Usage: game.py [OPTIONS]

  Generate multiple games for each game type passed.

Options:
  -t, --type [random|high-frequency|low-frequency]
                                  Game type. It can be multiple types at once.
  -n, --num-of-games INTEGER      Number of games generate for each type.
                                  [default: 1]

  --help                          Show this message and exit.
```

### Examples

- To generate only one game type:<br>
  `pipenv run game -t random`

- To generate multiple games for only one game type:<br>
  `pipenv run game -t random -n 5`

- To generate more than one game type:<br>
  `pipenv run game -t high-frequency -t low-frequency`

- To generate multiple games for more than one game type:<br>
  `pipenv run game -t high-frequency -t low-frequency -n 5`

---

## Rules to Generate Games

There are three types of game that can be generated:

1. Random
1. Based on high frequency
1. Based on low frequency

The `random` type generated a totally random game.

The `high frequency` gives more chance to be chosen for numbers and stars that have a **higher** frequency based on games stored in the database.

The `low frequency` gives more chance to be chosen for numbers and stars that have a **lower** frequency based on games stored in the database.

All games generated follow these rules:

1. Must not be a game already drawn in the past.
1. Must not contain only even or odd numbers (not applied on stars).

---

## Managing the Database

To check all commands available to manage the database execute: `pipenv run database --help`.

```text
$ pipenv run database --help
Usage: database.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  export       Export all results on the database to a CSV file.
  full-update  Update Euromillions results from last date stored until today.
  init         Initialize database.
  status       Show the database current status.
  update       Update Euromillions result for a given date.
```

### Commands to Manage the Database

#### Initialize database

```text
$ pipenv run database init --help
Usage: database.py init [OPTIONS]

  Initialize database.

  If --overwrite is used, the existing database will be deleted.

Options:
  --overwrite / --no-overwrite  Overwrite existing database.  [default: False]
  --help                        Show this message and exit.
```

#### Database status

```text
$ pipenv run database status --help
Usage: database.py status [OPTIONS]

  Show the database current status:
  - Number of results stored.
  - Last draw date stored.
  - Last results stored.

Options:
  --help  Show this message and exit.
```

#### Database single update

```text
$ pipenv run database update --help
Usage: database.py update [OPTIONS]

  Update Euromillions result for a given date.

  If --draw_date is not passed, it will update with the date of the first
  Euromillions result.

Options:
  --draw-date [%Y-%m-%d]  Date to get Euromillions draw numbers.  [default: 2004-02-13]
  --help                  Show this message and exit.
```

#### Database full update

```text
$ pipenv run database full-update --help
Usage: database.py full-update [OPTIONS]

  Update Euromillions results from last date stored until today.

Options:
  --max-days INTEGER  Runs the update for a maximun number of days
  --help              Show this message and exit.
```

#### Database export

```text
$ pipenv run database export --help
Usage: database.py export [OPTIONS]

  Export all results on the database to a CSV file.

Options:
  --filename TEXT  CSV filename, it can be an absolute path.
  --help           Show this message and exit.
```

---

License [MIT](https://opensource.org/licenses/MIT).

```text
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
