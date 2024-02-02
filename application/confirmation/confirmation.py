from __future__ import annotations

import itertools
from dataclasses import dataclass, field
from typing import Set, List, Collection, Any, Iterable

from more_itertools import consume

from application.trade import Deal
from . import message as msg
from .message import Message
from .type import Type


def confirm(trades: List[Deal], _type: Type = Type.REUTER) -> List[Confirmation]:
    entity_trades = deals_by_entity(trades)
    return [Confirmation.of(e, _type, t) for e, t in entity_trades.items()]


def deals_by_entity(trades: List[Deal]):
    bid_trades = {
        e: list(trades)
        for e, trades in itertools.groupby(
            sorted(trades, key=lambda t: t.bid), lambda t: t.bid
        )
    }
    offer_trades = {
        e: list(trades)
        for e, trades in itertools.groupby(
            sorted(trades, key=lambda t: t.offer), lambda t: t.offer
        )
    }
    return {
        e: bid_trades.get(e, []) + offer_trades.get(e, [])
        for e in set(bid_trades) | set(offer_trades)
    }


@dataclass
class Confirmation:
    entity: str
    type: Type
    messages: List[Message] = field(default_factory=list)
    raw_trades: List[Deal] = field(default_factory=list)
    trade_ids: Set[str] = field(init=False)

    def __post_init__(self) -> None:
        self.messages.sort(key=lambda m: m.body)
        self.trade_ids = set(t.trade_id for t in self.raw_trades)
        self.messages = self.to_messages(self.raw_trades)

    @staticmethod
    def of(entity: str, _type: Type, trades: Collection[Deal]):
        cfm = Confirmation(entity, _type)
        cfm.add_trades(trades)
        return cfm

    def to_messages(self, deals: Collection[Deal]) -> List[Message]:
        return [
            msg.to_message(self.entity, d.product, d, self.type)
            for d in deals
            if d.has_entity(self.entity)
        ]

    def add_message(self, m: Message) -> None:
        self.messages.append(m)

    def add_messages(self, msgs: Iterable[Message]) -> None:
        self.messages.extend(msgs)

    def add_trade(self, t: Any) -> None:
        self.add_trades([t])

    def add_trades(self, trades: Collection[Any]) -> None:
        consume(self.trade_ids.add(t.trade_id) for t in trades)
        self.raw_trades += trades
        messages = self.to_messages(trades)
        self.add_messages(messages)

    def general(self) -> str:
        # TODO: TBD
        pass

    def cx(self) -> str:
        return msg.rate_grouped(self.messages)

    def rx(self) -> str:
        # TODO: TBD
        pass
