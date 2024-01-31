from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from itertools import groupby
from typing import Set, List, Collection, Any, Iterable, Tuple, Callable

from jinja2 import Template as JTemplate
from more_itertools import consume


def to_cx_msg_str(messages: List[Message]):
    regulars, switches = split_switches(messages)
    return merge_messages_to_str(regulars, switches, _to_cx_msg_str)


def _to_cx_msg_str(messages: List[Message]):
    if not messages:
        return ""
    body = messages[0].body
    header = "\n".join(m.header for m in messages)
    return f"{header}\n{body}\n"


def split_switches(msgs: List[Message]) -> Tuple[List[Message], List[Message]]:
    regulars = [m for m in msgs if not m.switch]
    switches = [m for m in msgs if m.switch]
    return regulars, switches


def merge_messages_to_str(
    m1: List[Message],
    m2: List[Message],
    str_conversion_func: Callable[[List[Message]], str],
) -> str:
    m1_str = f"{str_conversion_func(m1)}" if m1 else ""
    m2_str = f"{str_conversion_func(m2)}" if m2 else ""
    joint = "\n" if m1_str and m2_str else ""
    return m1_str + joint + m2_str


class Format(Enum):
    FULL = "full"
    GENERAL = "general"
    CX = "cx"
    rx = "rx"


class Type(Enum):
    MESSENGER = "messenger"
    REUTER = "reuter"
    RTNS = "rtns"
    EMAIL = "email"
    PHONE = "phone"
    FAX = "fax"


@dataclass
class Method:
    entity: str
    product: str
    types: Set[Type] = field(default_factory=set)

    @staticmethod
    def of(
        entity: str,
        product: str,
        messenger: bool = False,
        reuter: bool = False,
        rtns: bool = False,
        email: bool = False,
        phone: bool = False,
        fax: bool = False,
    ) -> Method:
        method = Method(entity, product)
        if messenger:
            method.types.add(Type.MESSENGER)
        if reuter:
            method.types.add(Type.REUTER)
        if rtns:
            method.types.add(Type.RTNS)
        if email:
            method.types.add(Type.EMAIL)
        if phone:
            method.types.add(Type.PHONE)
        if fax:
            method.types.add(Type.FAX)
        return method

    @property
    def messenger(self) -> bool:
        return self._in_types(Type.MESSENGER)

    @property
    def reuter(self) -> bool:
        return self._in_types(Type.REUTER)

    @property
    def rtns(self) -> bool:
        return self._in_types(Type.RTNS)

    @property
    def email(self) -> bool:
        return self._in_types(Type.EMAIL)

    @property
    def phone(self) -> bool:
        return self._in_types(Type.PHONE)

    @property
    def fax(self) -> bool:
        return self._in_types(Type.FAX)

    def _in_types(self, _type: Type) -> bool:
        return _type in self.types


@dataclass
class Template:
    entity: str
    type: Type
    header: str
    body: str
    tail: str
    _header: JTemplate = field(init=False)
    _body: JTemplate = field(init=False)
    _tail: JTemplate = field(init=False)

    def __post_init__(self):
        self._header = JTemplate(self.header)
        self._body = JTemplate(self.body)
        if self.tail:
            self._tail = JTemplate(self.tail)

    def render_header(self, **kwargs):
        return self._header.render(**kwargs)

    def render_body(self, **kwargs):
        return self._body.render(**kwargs)

    def render_tail(self, **kwargs):
        if not self.tail:
            return ""
        return self._tail.render(**kwargs)

    def is_empty(self) -> bool:
        return not self.body


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


@dataclass
class Confirmation:
    entity: str
    type: Type
    messages: List[Message] = field(default_factory=list)
    raw_trades: List[Any] = field(default_factory=list)
    trade_ids: Set[str] = field(init=False)

    def __post_init__(self) -> None:
        self.messages.sort(key=lambda m: m.body)
        self.trade_ids = set(t.trade_id for t in self.raw_trades)
        self.messages = self._to_messages(self.raw_trades)

    def _to_messages(self, trades: Collection[Any]) -> List[Message]:
        # Override
        raise NotImplementedError

    def add_message(self, m: Message) -> None:
        self.messages.append(m)

    def add_messages(self, msgs: Iterable[Message]) -> None:
        self.messages.extend(msgs)

    def add_trade(self, t: Any) -> None:
        self.add_trades([t])

    def add_trades(self, trades: Collection[Any]) -> None:
        consume(self.trade_ids.add(t.trade_id) for t in trades)
        self.raw_trades += trades
        messages = self._to_messages(trades)
        self.add_messages(messages)

    def general(self) -> str:
        # TODO: TBD
        pass

    def cx(self) -> str:
        self.messages.sort(key=lambda m: m.entity)
        entity_grouped_messages = {
            e: list(msgs) for e, msgs in groupby(self.messages, lambda m: m.entity)
        }
        grouped_messages = [
            to_cx_msg_str(msgs)
            for entity, messages in entity_grouped_messages.items()
            for msgs in (
                list(msgs)
                for b, msgs in groupby(
                    sorted(messages, key=lambda m: m.body), lambda m: m.body
                )
            )
        ]
        return "\n".join(grouped_messages)

    def rx(self) -> str:
        # TODO: TBD
        pass
