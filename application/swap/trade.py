from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date

from utils import stringutils, dateutils
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
    bid_switch: bool = field(default=False)
    offer_switch: bool = field(default=False)
    _tenor: Tenor = field(init=False)
    product: str = field(default="swap")
    trade_id: str = field(default_factory=stringutils.generate_uuid)
    spot_date: date = field(init=False)

    def __post_init__(self):
        self._tenor = Tenor(self.tenor, self.trade_date)
        self.spot_date = dateutils.add_workdays(self.trade_date, 2)

    @property
    def first_leg(self) -> Leg:
        return self._tenor.near

    @property
    def second_leg(self) -> Leg:
        return self._tenor.far

    @property
    def bid_bro_fee(self) -> float:
        return 0 if self.bid_switch else round(self.bid_brokerage_fee)

    @property
    def offer_bro_fee(self) -> float:
        return 0 if self.offer_switch else round(self.offer_brokerage_fee)

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
            "tenor": self.tenor,
            "bid": self.bid,
            "offer": self.offer,
            "entity": entity,
            "margin": counter_party,
            "amount": str(round(self.amount, 2)),
            "near_rate": str(round(self.near_rate, 2)),
            "par_rate": str(round(self.par_rate, 2)),
            "bid_brokerage_fee": str(self.bid_bro_fee),
            "offer_brokerage_fee": str(self.offer_bro_fee),
            "deal_time": cfm_datetime(self.deal_time),
            "product": self.product,
            "spot_date": cfm_date(self.spot_date),
            "deal": deal,
            "direction": direction,
        }
