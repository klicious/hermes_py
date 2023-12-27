from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date

from .tenor import Tenor, Leg


@dataclass
class Trade:
    trade_date: date
    tenor: str
    bid: str
    offer: str
    margin: float
    amount: int
    near_rate: float
    par_rate: float
    bid_brokerage_fee: float
    offer_brokerage_fee: float
    deal_time: datetime = field(default_factory=datetime.now)
    _tenor: Tenor = field(init=False)
    product: str = field(default="swap")

    def __post_init__(self):
        self._tenor = Tenor(self.tenor, self.trade_date)

    @property
    def first_leg(self) -> Leg:
        return self._tenor.near

    @property
    def second_leg(self) -> Leg:
        return self._tenor.far
