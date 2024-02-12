from dataclasses import dataclass


@dataclass
class Fee:
    house: str
    currency: str
    amount: int
