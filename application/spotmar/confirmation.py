import itertools
from dataclasses import dataclass
from typing import List

from application import confirmation as cfm
from application.confirmation import Message, Type as ConfirmationType

PRODUCT = cfm.SPOT_MAR
from .trade import Trade


@dataclass
class Confirmation:
    entity: str
    type: ConfirmationType
    trade: Trade
    message: Message


def reuter(trades: List[Trade]):
    messages = sorted(
        itertools.chain.from_iterable(
            to_messages(t, ConfirmationType.REUTER) for t in trades
        ),
        key=lambda m: m.entity,
    )
    return {
        e: list(msgs) for e, msgs in itertools.groupby(messages, lambda m: m.entity)
    }


def to_messages(trade: Trade, _type: ConfirmationType) -> List[Message]:
    entity = trade.bid
    template = cfm.get_reuter_template(PRODUCT, entity)
    bid_message = Message(
        entity,
        _type,
        template.render_header(**trade.cfm_dict(entity)),
        template.render_body(**trade.cfm_dict(entity)),
        template.render_tail(**trade.cfm_dict(entity)),
    )
    entity = trade.offer
    template = cfm.get_reuter_template(PRODUCT, entity)
    offer_message = Message(
        entity,
        _type,
        template.render_header(**trade.cfm_dict(entity)),
        template.render_body(**trade.cfm_dict(entity)),
        template.render_tail(**trade.cfm_dict(entity)),
    )
    return [bid_message, offer_message]
