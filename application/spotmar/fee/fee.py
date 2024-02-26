from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Fee:
    house: str
    currency: str
    amount: int

    def __post_init__(self):
        self.house = self.house.upper()
        self.currency = self.currency.upper()
