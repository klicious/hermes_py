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
    bid_house: str
    offer_house: str
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
    deal_id: str = field(default_factory=stringutils.generate_uuid)
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

    def has_house(self, house: str) -> bool:
        return self.bid_house == house or self.offer_house == house

    def brokerage_fee(self, house):
        if house == self.bid_house:
            return self.bid_bro_fee
        if house == self.offer_house:
            return self.offer_bro_fee
        return 0

    def cfm_dict(self, house) -> dict:
        action, action_preposition, counter_party = cfm.action(
            house, self.bid_house, self.offer_house
        )
        return {
            "house": house,
            "counter_party": counter_party,
            "action": action,
            "action_preposition": action_preposition,
            "trade_date": cfm_date(self.trade_date),
            "product": self.product,
            "bid": self.bid_house,
            "offer": self.offer_house,
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
