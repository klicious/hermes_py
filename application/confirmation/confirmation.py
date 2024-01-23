from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Set

from jinja2 import Template as JTemplate


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

    @property
    def full(self) -> str:
        return f"{self.header}\n{self.body}\n{self.tail}"


@dataclass
class Confirmation:
    entity: str
    type: Type
    trade_id: str
    message: Message

    def general(self):
        # TODO: TBD
        pass

    def cx(self):
        # TODO: TBD
        pass

    def rx(self):
        # TODO: TBD
        pass
