from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date

from utils import stringutils, dateutils
from . import confirmation as cfm
from .tenor import Tenor, Leg


@dataclass
class Trade:
    type: str
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
        action, action_preposition, counter_party = cfm.action(
            entity, self.bid, self.offer
        )
        delivery = "ndf" if self.type == "ndf" else "delivery"
        return {
            "trade_date": cfm.date(self.trade_date),
            "tenor": self.tenor,
            "bid": self.bid,
            "offer": self.offer,
            "entity": entity,
            "counter_party": counter_party,
            "margin": cfm.rate(self.margin),
            "amount": cfm.amount(self.amount),
            "near_rate": cfm.rate(self.near_rate),
            "par_rate": cfm.rate(self.par_rate),
            "bid_brokerage_fee": cfm.amount(self.bid_bro_fee),
            "offer_brokerage_fee": cfm.amount(self.offer_bro_fee),
            "deal_date": cfm.date(self.deal_time.date()),
            "deal_datetime": cfm.datetime(self.deal_time),
            "deal_time": cfm.time(self.deal_time.time()),
            "product": self.product,
            "spot_date": cfm.date(self.spot_date),
            "action": action,
            "action_preposition": action_preposition,
            "delivery": delivery,
            "near_vfm_dates": cfm.vfm_dates(self._tenor.near.vfm_dates),
            "far_vfm_dates": cfm.vfm_dates(self._tenor.far.vfm_dates),
        }
