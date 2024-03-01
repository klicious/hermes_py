from __future__ import annotations

from dataclasses import dataclass, field

from adapter.google import sheets
from utils import stringutils

_NICKNAME_TO_BROKER = {}
_HOUSE_TO_BROKER = {}
_HOUSE_TO_ASSIGNMENT = {}


@dataclass
class Broker:
    team: str
    rank: str
    name: str
    nickname: str
    id: str = field(default_factory=stringutils.generate_uuid)

    @property
    def full_title(self):
        return f"{self.name} {self.rank}"


@dataclass
class HouseAssignment:
    house: str
    broker: str
    backup: str
    backup2: str


def init():
    __load_brokers()


def refresh():
    init()


def __load_brokers():
    brokers = [Broker(**t) for t in sheets.get_values("brokers", "A:D")]
    nickname_to_broker = {t.nickname: t for t in brokers}
    _NICKNAME_TO_BROKER.update(nickname_to_broker)


def __load_house_assignments():
    house_assignments = [
        HouseAssignment(**hta) for hta in sheets.get_values("house to broker", "A:D")
    ]
    house_to_assignment = {t.nickname: t for t in house_assignments}
    _HOUSE_TO_ASSIGNMENT.update(house_to_assignment)


def get_broker(nickname: str):
    if not _NICKNAME_TO_BROKER:
        init()
    return _NICKNAME_TO_BROKER.get(nickname)


def get_brokers():
    if not _NICKNAME_TO_BROKER:
        init()
    return list(_NICKNAME_TO_BROKER.values())


def get_house_assignment(house: str):
    if not _HOUSE_TO_ASSIGNMENT:
        init()
    return _HOUSE_TO_ASSIGNMENT.get(house)


def get_house_assignments():
    if not _HOUSE_TO_ASSIGNMENT:
        init()
    return list(_HOUSE_TO_BROKER.values())
