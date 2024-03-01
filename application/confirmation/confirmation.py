from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Set, List, Collection, Iterable

from more_itertools import consume

from application.trade import Deal
from . import message as msg
from .message import Message
from .type import Type


def confirm(trades: List[Deal], _type: Type = Type.REUTER) -> List[Confirmation]:
    house_to_deals = deals_by_house(trades)
    return [Confirmation.of(e, _type, t) for e, t in house_to_deals.items()]


def deals_by_house(trades: List[Deal]):
    bid_trades = {
        e: list(trades)
        for e, trades in itertools.groupby(
            sorted(trades, key=lambda t: t.bid_house), lambda t: t.bid_house
        )
    }
    offer_trades = {
        e: list(trades)
        for e, trades in itertools.groupby(
            sorted(trades, key=lambda t: t.offer_house), lambda t: t.offer_house
        )
    }
    return {
        e: bid_trades.get(e, []) + offer_trades.get(e, [])
        for e in set(bid_trades) | set(offer_trades)
    }


@dataclass
class Confirmation:
    house: str
    type: Type
    messages: List[Message] = field(default_factory=list)
    raw_deals: List[Deal] = field(default_factory=list)
    deal_ids: Set[str] = field(init=False)

    def __post_init__(self) -> None:
        assert all(m.house == self.house for m in self.messages)
        self.messages.sort(key=lambda m: m.body)
        self.deal_ids = set(t.deal_id for t in self.raw_deals)
        self.messages = self.to_messages(self.raw_deals)

    @staticmethod
    def of(house: str, _type: Type, deals: Collection[Deal]):
        cfm = Confirmation(house.upper(), _type)
        cfm.add_deals(deals)
        return cfm

    def to_messages(self, deals: Collection[Deal]) -> List[Message]:
        return [
            msg.to_message(self.house, d.product, d, self.type)
            for d in deals
            if d.has_house(self.house)
        ]

    def add_message(self, m: Message) -> None:
        self.messages.append(m)

    def add_messages(self, msgs: Iterable[Message]) -> None:
        self.messages.extend(msgs)

    def add_deal(self, t: Deal) -> None:
        self.add_deals([t])

    def add_deals(self, deals: Collection[Deal]) -> None:
        consume(self.deal_ids.add(t.deal_id) for t in deals)
        self.raw_deals += deals
        messages = self.to_messages(deals)
        self.add_messages(messages)

    def individual(self) -> str:
        deals = {d.deal_id: d for d in self.raw_deals}
        return msg.individual(self.messages, deals)

    def general(self) -> str:
        deals = {d.deal_id: d for d in self.raw_deals}
        return msg.rate_grouped(self.messages, deals)

    def rx(self) -> str:
        # TODO: TBD
        pass
