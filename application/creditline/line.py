from __future__ import annotations
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

MAX_CREDIT = 1_000_000
SYMBOL_TO_AMOUNT = {
    "B": 100,
    "M": 50,
    "S": 10,
    "X": 0,
    "O": MAX_CREDIT,
}


def _max_amount_from_symbol(symbol: str) -> int:
    if "chk" in symbol:
        return int(symbol.replace("chk", "").strip())
    stripped_symbol = symbol.strip().upper()
    if stripped_symbol.isnumeric():
        return int(stripped_symbol)
    return SYMBOL_TO_AMOUNT.get(stripped_symbol, 0)


class AVAILABILITY(Enum):
    OPEN = "open"
    CLOSED = "closed"
    NEED_CHECK = "check required"


@dataclass
class CreditLine:
    source: str
    destination: str
    product: str
    tenor: str
    symbol: str
    max: int = field(default=0)
    used: int = field(default=0)
    can_switch: bool = field(default=False)
    allows_switch: bool = field(default=False)
    last_modified_datetime: datetime = field(default_factory=datetime.now)
    registered_datetime: datetime = field(default_factory=datetime.now)

    @staticmethod
    def of(
        source: str,
        destination: str,
        product: str,
        tenor: str,
        symbol: str,
        can_switch: bool = False,
        allows_switch: bool = True,
    ) -> CreditLine:
        return CreditLine(
            source=source,
            destination=destination,
            product=product,
            tenor=tenor,
            symbol=symbol,
            max=_max_amount_from_symbol(symbol),
            can_switch=can_switch,
            allows_switch=allows_switch,
        )

    @property
    def remaining(self) -> int:
        return self.max - self.used

    @property
    def is_open(self) -> bool:
        return 0 < self.remaining

    @property
    def is_closed(self):
        return not self.is_open

    @property
    def availability(self):
        if "chk" in self.symbol:
            return AVAILABILITY.CLOSED.NEED_CHECK
        return AVAILABILITY.OPEN if self.remaining > 0 else AVAILABILITY.CLOSED

    def open(self, amount: int) -> CreditLine:
        self.max = amount
        return self

    def close(self) -> CreditLine:
        self.max = 0
        return self

    def uncertain(self, amount: int) -> CreditLine:
        self.max = amount
        self.symbol = "chk"
        return self

    def use(self, amount: int) -> CreditLine:
        if amount <= self.remaining:
            self.used += amount
        return self

    def reset_credit(self) -> CreditLine:
        self.used = 0
        return self
