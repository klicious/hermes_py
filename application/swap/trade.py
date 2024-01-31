from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date

from utils import stringutils
from .tenor import Tenor, Leg


def cfm_date(d: date) -> str:
    return d.isoformat()


def cfm_datetime(dt: datetime) -> str:
    return dt.isoformat()


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
    switch: bool = field(default=False)
    _tenor: Tenor = field(init=False)
    product: str = field(default="swap")
    trade_id: str = field(default_factory=stringutils.generate_uuid)

    def __post_init__(self):
        self._tenor = Tenor(self.tenor, self.trade_date)

    @property
    def first_leg(self) -> Leg:
        return self._tenor.near

    @property
    def second_leg(self) -> Leg:
        return self._tenor.far

    def cfm_dict(self, entity) -> dict:
        if entity == self.bid:
            deal = "buy"
            direction = "from"
            counter_party = self.offer
        else:
            deal = "sell"
            direction = "to"
            counter_party = self.bid
        return {
            "trade_date": cfm_date(self.trade_date),
            "tenor": self.bid,
            "bid": self.offer,
            "offer": entity,
            "margin": counter_party,
            "amount": str(round(self.price, 2)),
            "near_rate": str(round(self.amount, 2)),
            "par_rate": str(round(self.rate, 2)),
            "bid_brokerage_fee": cfm_date(self.value_date),
            "offer_brokerage_fee": str(round(self.mar, 2)),
            "deal_time": str(self.bid_bro_fee),
            "product": self.product,
            "spot_date": cfm_date(self.spot_date),
            "deal": deal,
            "direction": direction,
        }
