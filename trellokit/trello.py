import typing
import urllib

import httpx
from pydantic import BaseModel


class Board(BaseModel):
    id: str
    name: str
    url: str
    shortUrl: str


class List(BaseModel):
    id: str
    name: str
    closed: bool
    idBoard: str
    pos: float
    subscribed: bool


class Label(BaseModel):
    id: str
    idBoard: str
    name: str
    color: str

    def __str__(self):
        return self.name


class Badges(BaseModel):
    due: typing.Optional[str]
    start: typing.Optional[str]


class Card(BaseModel):
    id: str
    name: str
    labels: typing.List[Label]
    badges: Badges
    start: typing.Optional[str]
    dateLastActivity: str


class Boards:
    
    def __init__(self, api_key: str, api_token: str, api_url: str = "https://api.trello.com/1/members/me/boards"):
        self.api_key = api_key
        self.api_token = api_token
        self.api_url = api_url

    def list(self):
        params = {
            "key": self.api_key,
            "token": self.api_token
        }

        url = "?".join([self.api_url, urllib.parse.urlencode(params)])

        resp = httpx.get(url)
        if resp.status_code != 200:
            raise Exception(resp.text)

        boards = []
        for entry in resp.json():
            boards.append(Board.model_validate(entry))

        return boards


class Lists:
    
    def __init__(self, api_key: str, api_token: str, api_url: str = "https://api.trello.com/1/lists/{id}/cards"):
        self.api_key = api_key
        self.api_token = api_token
        self.api_url = api_url

    def list_by_board_id(self, board_id: str):
        params = {
            "key": self.api_key,
            "token": self.api_token
        }

        url = "?".join([
            "https://api.trello.com/1/boards/{id}/lists".format(id=board_id),
            urllib.parse.urlencode(params),
        ])

        resp = httpx.get(url)
        if resp.status_code != 200:
            raise Exception(resp.text)


        boards = []
        for entry in resp.json():
            boards.append(List.model_validate(entry))

        return boards


class Cards:
    
    def __init__(self, api_key: str, api_token: str, api_url: str = "https://api.trello.com/1/lists/{id}/cards"):
        self.api_key = api_key
        self.api_token = api_token
        self.api_url = api_url

    def list(self, list_id: str, label: str = None):
        params = {
            "key": self.api_key,
            "token": self.api_token
        }

        url = "?".join([
            "https://api.trello.com/1/lists/{id}/cards".format(id=list_id),
            urllib.parse.urlencode(params),
        ])

        resp = httpx.get(url)
        if resp.status_code != 200:
            raise Exception(resp.text)

        cards = []
        for entry in resp.json():
            cards.append(Card.model_validate(entry))

        if label:
            cards = [c for c in cards if label in [l.name for l in c.labels]]

        return cards
