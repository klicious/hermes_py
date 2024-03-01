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

    def sum(self, quantity: int):
        return quantity * self.amount
