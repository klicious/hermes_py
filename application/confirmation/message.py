from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import groupby
from typing import List, Tuple, Callable, Dict

from application.trade import Deal
from . import data
from .template import Template
from .type import Type


def group_by_entity(msgs: List[Message]) -> Dict[str, List[Message]]:
    msgs.sort(key=lambda m: m.entity)
    return {e: list(msgs) for e, msgs in groupby(msgs, lambda m: m.entity)}


def individual(messages: List[Message]) -> Dict[str, str]:
    entity_msgs_dict = group_by_entity(messages)
    return {
        e: convert_messages_to_str(msgs, __individual_msg_str)
        for e, msgs in entity_msgs_dict.items()
    }


def __individual_msg_str(messages: List[Message]) -> str:
    if not messages:
        return ""
    return "\n".join(m.full for m in messages)


def rate_grouped(messages: List[Message]) -> Dict[str, str]:
    entity_grouped_messages = group_by_entity(messages)
    return {
        entity: convert_messages_to_str(msgs, __rate_grouped_msg_str)
        for entity, messages in entity_grouped_messages.items()
        for msgs in (
            list(msgs)
            for b, msgs in groupby(
                sorted(messages, key=lambda m: m.body), lambda m: m.body
            )
        )
    }


def __rate_grouped_msg_str(messages: List[Message]) -> str:
    if not messages:
        return ""
    body = messages[0].body
    header = "\n".join(m.header for m in messages)
    return f"{header}\n{body}\n"


def split_switches(msgs: List[Message]) -> Tuple[List[Message], List[Message]]:
    regulars = [m for m in msgs if not m.switch]
    switches = [m for m in msgs if m.switch]
    return regulars, switches


def convert_messages_to_str(
    messages: List[Message], str_conversion_func: Callable[[List[Message]], str]
) -> str:
    regulars, switches = split_switches(messages)
    return __merge_messages_to_str(regulars, switches, str_conversion_func)


def __merge_messages_to_str(
    m1: List[Message],
    m2: List[Message],
    str_conversion_func: Callable[[List[Message]], str],
) -> str:
    m1_str = f"{str_conversion_func(m1)}" if m1 else ""
    m2_str = f"{str_conversion_func(m2)}" if m2 else ""
    joint = "\n" if m1_str and m2_str else ""
    return m1_str + joint + m2_str


def to_message(entity: str, product: str, deal: Deal, _type: Type) -> Message | None:
    template: Template = data.get_reuter_template(product, entity)
    switch: bool = (
        deal.bid == entity
        and deal.bid_switch
        or deal.offer == entity
        and deal.offer_switch
    )
    return Message(
        entity,
        _type,
        template.render_header(**deal.cfm_dict(entity)),
        template.render_body(**deal.cfm_dict(entity)),
        template.render_tail(**deal.cfm_dict(entity)),
        switch=switch,
    )


class Format(Enum):
    FULL = "full"
    GENERAL = "general"
    CX = "cx"
    rx = "rx"


@dataclass
class Message:
    entity: str
    type: Type
    header: str
    body: str
    tail: str
    switch: bool = field(default=False)

    @property
    def full(self) -> str:
        return f"{self.header}\n{self.body}\n{self.tail}"
