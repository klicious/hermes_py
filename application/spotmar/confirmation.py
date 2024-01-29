from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import List, Collection

from application import confirmation as cfm
from application.confirmation import (
    Message,
    Type as ConfirmationType,
    Confirmation as GeneralConfirmation,
)

PRODUCT = cfm.SPOT_MAR
from .trade import Trade


def confirm(
        trades: List[Trade], _type: ConfirmationType = ConfirmationType.REUTER
) -> List[Confirmation]:
    entity_trades = trades_by_entity(trades)
    return [Confirmation.of(e, _type, t) for e, t in entity_trades.items()]


def reuter(trades: List[Trade]):
    messages = sorted(
        itertools.chain.from_iterable(
            to_message(t, ConfirmationType.REUTER) for t in trades
        ),
        key=lambda m: m.entity,
    )
    return {
        e: list(msgs) for e, msgs in itertools.groupby(messages, lambda m: m.entity)
    }


def trades_by_entity(trades: List[Trade]):
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


def to_message(entity: str, trade: Trade, _type: ConfirmationType) -> Message | None:
    template = cfm.get_reuter_template(PRODUCT, entity)
    return Message(
        entity,
        _type,
        template.render_header(**trade.cfm_dict(entity)),
        template.render_body(**trade.cfm_dict(entity)),
        template.render_tail(**trade.cfm_dict(entity)),
        switch=trade.switch,
    )


@dataclass
class Confirmation(GeneralConfirmation):
    @staticmethod
    def of(entity: str, _type: ConfirmationType, trades: Collection[Trade]):
        cfm = Confirmation(entity, _type)
        cfm.add_trades(trades)
        return cfm

    def _to_messages(self, trades: Collection[Trade]) -> List[Message]:
        return [to_message(self.entity, t, self.type) for t in trades if t.has_entity(self.entity)]
