from __future__ import annotations
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

MAX_CREDIT = 1_000_000


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
    max: int
    used: int = field(default=0)
    availability: AVAILABILITY = field(default=AVAILABILITY.CLOSED)
    can_switch: bool = field(default=False)
    allows_switch: bool = field(default=False)
    last_modified_datetime: datetime = field(default_factory=datetime.now)
    registered_datetime: datetime = field(default_factory=datetime.now)

    @property
    def remaining(self) -> int:
        return self.max - self.used

    @property
    def is_open(self) -> bool:
        return 0 < self.remaining

    @property
    def is_closed(self):
        return not self.is_open

    def open(self, amount: int) -> CreditLine:
        self.max = amount
        self.availability = AVAILABILITY.OPEN
        return self

    def close(self) -> CreditLine:
        self.max = 0
        self.availability = AVAILABILITY.CLOSED
        return self

    def uncertain(self, amount: int) -> CreditLine:
        self.max = amount
        self.availability = AVAILABILITY.NEED_CHECK
        return self

    def set_switchable(self, switchable: bool) -> CreditLine:
        self.switchable = switchable
        return self

    def use(self, amount: int) -> CreditLine:
        if amount <= self.remaining:
            self.used += amount
        return self

    def reset_credit(self) -> CreditLine:
        self.used = 0
        return self
