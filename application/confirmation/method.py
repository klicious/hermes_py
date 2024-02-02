from __future__ import annotations

from dataclasses import dataclass, field
from typing import Set

from .type import Type


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
