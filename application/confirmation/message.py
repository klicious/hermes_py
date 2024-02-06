from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import groupby
from typing import List, Tuple, Callable, Dict

from application.trade import Deal
from utils import numberutils
from . import data
from .template import Template
from .type import Type


def group_by_entity(msgs: List[Message]) -> Dict[str, List[Message]]:
    msgs.sort(key=lambda m: m.house)
    return {e: list(msgs) for e, msgs in groupby(msgs, lambda m: m.house)}


def individual(messages: List[Message], deals: Dict[str, Deal]) -> str:
    entity_msgs_dict = group_by_entity(messages)
    return "\n".join(
        convert_messages_to_str(msgs, deals, __individual_msg_str)
        for e, msgs in entity_msgs_dict.items()
    )


def __individual_msg_str(messages: List[Message], deals: Dict[str, Deal]) -> str:
    if not messages:
        return ""
    return "\n".join(m.full for m in messages)


def rate_grouped(messages: List[Message], deals: Dict[str, Deal]) -> str:
    entity_grouped_messages = group_by_entity(messages)
    return "\n".join(
        convert_messages_to_str(msgs, deals, __rate_grouped_msg_str)
        for entity, messages in entity_grouped_messages.items()
        for msgs in (
            list(msgs)
            for b, msgs in groupby(
                sorted(messages, key=lambda m: m.body), lambda m: m.body
            )
        )
    )


def __rate_grouped_msg_str(messages: List[Message], deals: Dict[str, Deal]) -> str:
    if not messages:
        return ""
    body = messages[0].body
    header = "\n".join(m.header for m in messages)
    _brokerage_fee = sum(deals.get(m.deal_id).brokerage_fee(m.house) for m in messages)
    tail = messages[0].tail_bro_fee(_brokerage_fee)
    nl = "\n" if tail else ""
    return f"{header}\n{body}\n{tail}{nl}"


def split_switches(msgs: List[Message]) -> Tuple[List[Message], List[Message]]:
    regulars = [m for m in msgs if not m.switch]
    switches = [m for m in msgs if m.switch]
    return regulars, switches


def convert_messages_to_str(
    messages: List[Message],
    deals: Dict[str, Deal],
    str_conversion_func: Callable[[List[Message], Dict[str, Deal]], str],
) -> str:
    regulars, switches = split_switches(messages)
    return __merge_messages_to_str(regulars, switches, deals, str_conversion_func)


def __merge_messages_to_str(
    m1: List[Message],
    m2: List[Message],
    deals: Dict[str, Deal],
    str_conversion_func: Callable[[List[Message], Dict[str, Deal]], str],
) -> str:
    m1_str = f"{str_conversion_func(m1, deals)}" if m1 else ""
    m2_str = f"{str_conversion_func(m2, deals)}" if m2 else ""
    joint = "\n" if m1_str and m2_str else ""
    return m1_str + joint + m2_str


def to_message(house: str, product: str, deal: Deal, _type: Type) -> Message | None:
    template: Template = data.get_template(product, house, _type)
    switch: bool = (
        deal.bid_house == house
        and deal.bid_switch
        or deal.offer_house == house
        and deal.offer_switch
    )
    cfm_dict = deal.cfm_dict(house)
    cfm_dict["brokerage_fee_msg"] = brokerage_fee(deal.brokerage_fee(house))
    return Message(
        deal.deal_id,
        product,
        house,
        _type,
        template.render_header(**cfm_dict),
        template.render_body(**cfm_dict),
        template.render_tail(**cfm_dict),
        switch=switch,
    )


def brokerage_fee(fee: float, currency: str = "krw"):
    return (
        f"bro {currency} {numberutils.accounting_format(fee)}"
        if fee
        else "no brokerage"
    )


class Format(Enum):
    FULL = "full"
    GENERAL = "general"
    CX = "cx"
    rx = "rx"


@dataclass
class Message:
    deal_id: str
    product: str
    house: str
    type: Type
    header: str
    body: str
    tail: str
    switch: bool = field(default=False)

    @property
    def full(self) -> str:
        return f"{self.header}\n{self.body}\n{self.tail}"

    def tail_bro_fee(self, fee: float, currency: str = "krw") -> str:
        template: Template = data.get_template(self.product, self.house, self.type)
        bro_fee_msg = brokerage_fee(fee, currency)
        return template.render_tail(**{"brokerage_fee_msg": bro_fee_msg})
