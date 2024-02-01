from dataclasses import dataclass, field
from datetime import date, datetime

from utils import dateutils, stringutils


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
    def bid_bro_fee(self):
        return 0 if self.bid_switch else round(self.bid_brokerage_fee)

    @property
    def offer_bro_fee(self):
        return 0 if self.offer_switch else round(self.offer_brokerage_fee)

    def has_entity(self, entity: str) -> bool:
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
            "trade_date": cfm_date(self.trade_date),
            "bid": self.bid,
            "offer": self.offer,
            "entity": entity,
            "counter_party": counter_party,
            "price": str(round(self.price, 2)),
            "amount": str(round(self.amount, 2)),
            "rate": str(round(self.rate, 2)),
            "value_date": cfm_date(self.value_date),
            "mar": str(round(self.mar, 2)),
            "bid_brokerage_fee": str(self.bid_bro_fee),
            "offer_brokerage_fee": str(self.offer_bro_fee),
            "deal_time": cfm_datetime(self.deal_time),
            "switch": str(self.switch),
            "trader": self.trader,
            "bid_their_to": self.bid_their_to,
            "offer_their_to": self.offer_their_to,
            "product": self.product,
            "spot_date": cfm_date(self.spot_date),
            "deal": deal,
            "direction": direction,
        }
