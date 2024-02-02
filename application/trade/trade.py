from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import Protocol

from utils import stringutils


def cfm_date(d: date) -> str:
    return d.isoformat()


def cfm_datetime(dt: datetime) -> str:
    return dt.isoformat()


def cfm_time(t: time) -> str:
    return t.isoformat()


@dataclass
class Deal(Protocol):
    product: str
    bid: str
    offer: str
    price: float
    amount: float
    deal_datetime: datetime
    bid_brokerage_fee: float
    offer_brokerage_fee: float
    bid_switch: bool = field(
        default=False
    )  # means the bidding entity is doing the switch
    offer_switch: bool = field(
        default=False
    )  # means the offering entity is doing the switch
    trade_id: str = field(default_factory=stringutils.generate_uuid)

    @property
    def deal_date(self) -> date:
        return self.deal_datetime.date()

    @property
    def deal_time(self) -> time:
        return self.deal_datetime.time()

    @property
    def bid_bro_fee(self):
        return 0 if self.bid_switch else round(self.bid_brokerage_fee)

    @property
    def offer_bro_fee(self):
        return 0 if self.offer_switch else round(self.offer_brokerage_fee)

    def has_entity(self, entity) -> bool:
        return self.bid == entity or self.offer == entity

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
            "entity": entity,
            "product": self.product,
            "bid": self.bid,
            "offer": self.offer,
            "price": self.price,
            "amount": self.amount,
            "deal_datetime": cfm_datetime(self.deal_datetime),
            "deal_date": cfm_date(self.deal_date),
            "deal_time": cfm_time(self.deal_time),
            "bid_brokerage_fee": str(self.bid_bro_fee),
            "offer_brokerage_fee": str(self.offer_bro_fee),
            "bid_switch": self.bid_switch,
            "offer_switch": self.offer_switch,
            "trade_id": str(self.trade_id),
            "deal": deal,
            "direction": direction,
            "counter_party": counter_party,
        }
