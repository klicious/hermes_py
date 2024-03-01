from __future__ import annotations

from dataclasses import dataclass, field

from adapter.google import sheets
from utils import stringutils

_TRADERS = set()
_NICKNAME_TO_TRADER = {}


@dataclass
class Trader:
    house: str
    entity: str
    english_name: str
    name: str
    nickname: str
    rank: str
    email: str
    messenger: str
    id: str = field(default_factory=stringutils.generate_uuid)

    def __post_init__(self):
        self.house = self.house.upper()
        self.entity = self.entity.upper()
        self.english_name = self.english_name.upper()
        self.name = self.name.upper()
        self.nickname = self.nickname.upper()
        self.rank = self.rank.upper()
        self.email = self.email.upper()
        self.messenger = self.messenger.upper()

    def __eq__(self, other):
        if not isinstance(other, Trader):
            return NotImplemented
        return (
            self.house,
            self.entity,
            self.english_name,
            self.name,
            self.nickname,
            self.rank,
            self.email,
            self.messenger,
        ) == (
            other.house,
            other.entity,
            other.english_name,
            other.name,
            other.nickname,
            other.rank,
            other.email,
            other.messenger,
        )

    @property
    def full_title(self):
        return f"{self.name} {self.rank}"


def init():
    __load_traders()


def refresh():
    init()


def __load_traders():
    traders = [Trader(**t) for t in sheets.get_values("traders", "A:J")]
    nickname_to_trader = {t.nickname: t for t in traders}
    _NICKNAME_TO_TRADER.update(nickname_to_trader)
    _TRADERS.add(traders)


def get_trader(nickname: str):
    if not _NICKNAME_TO_TRADER:
        init()
    return _NICKNAME_TO_TRADER.get(nickname)


def get_traders_by_house(house: str, entity: str = "sl"):
    if not _TRADERS:
        init()
    return [
        t for t in _TRADERS if t.house == house.upper() and t.house == entity.upper()
    ]
