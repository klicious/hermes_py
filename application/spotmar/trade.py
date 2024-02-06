from dataclasses import dataclass, field
from datetime import date, datetime

from utils import dateutils, stringutils
from . import confirmation as cfm


def cfm_date(d: date) -> str:
    return d.isoformat()


def cfm_datetime(dt: datetime) -> str:
    return dt.isoformat()


@dataclass
class Trade:
    trade_date: date
    bid: str
    offer: str
    price: float
    amount: int
    rate: float
    value_date: date
    mar: float
    bid_brokerage_fee: float
    offer_brokerage_fee: float
    deal_time: datetime
    bid_switch: bool = field(default=False)
    offer_switch: bool = field(default=False)
    trader: str = field(default=None)
    bid_their_to: str = field(default=None)
    offer_their_to: str = field(default=None)
    product: str = field(default="spotmar")
    trade_id: str = field(default_factory=stringutils.generate_uuid)
    spot_date: date = field(init=False)

    def __post_init__(self):
        self.spot_date = dateutils.add_workdays(self.trade_date, 2)

    @property
    def deal_date(self) -> date:
        return self.deal_time.date()

    @property
    def bid_bro_fee(self):
        return 0 if self.bid_switch else self.bid_brokerage_fee

    @property
    def offer_bro_fee(self):
        return 0 if self.offer_switch else self.offer_brokerage_fee

    def has_entity(self, entity: str) -> bool:
        return self.bid == entity or self.offer == entity

    def cfm_dict(self, entity) -> dict:
        action, action_preposition, counter_party = cfm.action(
            entity, self.bid, self.offer
        )
        return {
            "entity": entity,
            "counter_party": counter_party,
            "action": action,
            "action_preposition": action_preposition,
            "trade_date": cfm_date(self.trade_date),
            "product": self.product,
            "bid": self.bid,
            "offer": self.offer,
            "price": cfm.amount(self.price),
            "amount": cfm.amount(self.amount),
            "rate": cfm.rate(self.rate),
            "value_date": cfm_date(self.value_date),
            "mar": cfm.rate(self.mar),
            "bid_brokerage_fee": cfm.amount(self.bid_bro_fee),
            "offer_brokerage_fee": cfm.amount(self.offer_bro_fee),
            "deal_time": cfm_datetime(self.deal_time),
            "bid_switch": self.bid_switch,
            "offer_switch": self.offer_switch,
            "trader": self.trader,
            "bid_their_to": self.bid_their_to,
            "offer_their_to": self.offer_their_to,
            "spot_date": cfm_date(self.spot_date),
        }
