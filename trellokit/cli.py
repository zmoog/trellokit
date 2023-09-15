import datetime
import io
import itertools
import typing

import click
from rich import box
from rich.console import Console
from rich.table import Table

from .trello import Boards, Lists, Cards, Card

@click.group()
@click.version_option()
@click.option(
    "--key",
    help="Trello API key",
    envvar="TRELLO_KEY",
    required=True,
)
@click.option(
    "--token",
    help="Trello API token",
    envvar="TRELLO_TOKEN",
    required=True,
)
@click.pass_context
def cli(ctx: click.Context, key: str, token: str):
    "CLI tool and Python library to access and use Trello API"
    ctx.ensure_object(dict)
    ctx.obj["key"] = key
    ctx.obj["token"] = token

#
# Boards
#

@cli.group(name="boards")
def boards():
    "Trello boards related commands"
    pass


@boards.command(name="list")
@click.pass_context
def list_boards(ctx: click.Context):
    "Command description goes here"
    boards = Boards(
        api_key=ctx.obj["key"],
        api_token=ctx.obj["token"],
    )

    for board in boards.list():
        click.echo(board.id + " " + board.name)

#
# Lists
#

@cli.group(name="lists")
def lists():
    "Trello lists related commands"
    pass


@lists.command(name="list")
@click.option(
    "--board-id",
    required=True,
)
@click.pass_context
def list_list(ctx: click.Context, board_id: str):
    "Command description goes here"
    lists = Lists(
        api_key=ctx.obj["key"],
        api_token=ctx.obj["token"],
    )

    for _list in lists.list_by_board_id(board_id):
        click.echo(_list.id + " " + _list.name)

#
# Cards
#

@cli.group(name="cards")
def cards():
    "Trello cards related commands"
    pass


@cards.command(name="list")
@click.option(
    "--list-id",
    required=True,
)
@click.option(
    "--label"
)
@click.pass_context
def list_cards(ctx: click.Context, list_id: str, label: str = None):
    "Command description goes here"
    cards = Cards(
        api_key=ctx.obj["key"],
        api_token=ctx.obj["token"],
    )

    card_list = cards.list(list_id)

    if label:
        card_list = [c for c in card_list if label in [l.name for l in c.labels]]

    # def by_labels(card: Card):
    #     return ",".join([l.name for l in card.labels]) if card.labels else "none"

    by_labels = By("labels")

    grouped = itertools.groupby(
        sorted(card_list, key=by_labels), key=by_labels
    )
    for labels, cards in grouped:
        _render_cards(list(cards), title=f"Cards with labels: {labels}")

    # _render_cards(sorted(cards.list(list_id), key=by_labels))

class By:
    def __init__(self, name: str):
        self.name = name
    def __call__(self, obj: typing.Any):
        v = getattr(obj, self.name)

        if isinstance(v, typing.List):
            # Turn list into a string using the string representation
            # of each element.
            return "".join(str(x) for x in v)

        return str(v)


def _render_cards(cards: typing.List[Card], title: str = "Cards"):

    table = Table(title=title, box=box.SIMPLE)
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Labels")
    table.add_column("Start")
    table.add_column("Age")
    table.add_column("Last Activity")

    now = datetime.datetime.now()

    for e in cards:

        # calculate age of entry
        if e.start:
            start = datetime.datetime.strptime(e.start, "%Y-%m-%dT%H:%M:%S.%fZ")

            # calculate the card age
            age = now - start

            # format timedelta to the number of days
            age = str(age.days) + " days"
        else:
            age = "non started yet"

        table.add_row(
            e.id,
            e.name,
            ",".join([l.name for l in e.labels]) if e.labels else "",
            e.start,
            age,
            str((now - datetime.datetime.strptime(e.dateLastActivity, "%Y-%m-%dT%H:%M:%S.%fZ")).days) + " days ago (" + e.dateLastActivity + ")",
        )


    # make footer with total duration visible
    table.show_footer = True

    # turn table into a string using the Console
    console = Console(file=io.StringIO())
    console.print(table)

    click.echo(console.file.getvalue())
