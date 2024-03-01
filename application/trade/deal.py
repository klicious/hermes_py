from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import Protocol

from utils import stringutils
from . import confirmation as cfm


@dataclass
class Deal(Protocol):
    product: str
    bid_house: str
    bid_entity: str
    offer_house: str
    offer_entity: str
    price: float
    amount: float
    deal_datetime: datetime
    bid_brokerage_fee: float
    offer_brokerage_fee: float
    trader: str
    bid_switch: bool = field(
        default=False
    )  # means the bidding entity is doing the switch
    offer_switch: bool = field(
        default=False
    )  # means the offering entity is doing the switch
    deal_id: str = field(default_factory=stringutils.generate_uuid)

    def __post_init__(self):
        self.product = self.product.strip().upper()
        self.bid_house = self.bid_house.strip().upper()
        self.bid_entity = self.bid_entity.strip().upper()
        self.offer_house = self.offer_house.strip().upper()
        self.offer_entity = self.offer_entity.strip().upper()
        self.trader = self.trader.strip().upper()

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

    def brokerage_fee(self, house: str):
        if house == self.bid_house:
            return self.bid_bro_fee
        if house == self.offer_house:
            return self.offer_bro_fee
        return 0

    def has_house(self, house: str) -> bool:
        h = house.upper()
        return self.bid_house == h or self.offer_house == h

    def cfm_dict(self, house: str) -> dict:
        action, action_preposition, counter_party = cfm.action(
            house, self.bid_house, self.offer_house
        )
        return {
            "house": house,
            "counter_party": counter_party,
            "action": action,
            "action_preposition": action_preposition,
            "product": self.product,
            "bid": self.bid_house,
            "offer": self.offer_house,
            "price": self.price,
            "amount": self.amount,
            "deal_datetime": cfm.datetime(self.deal_datetime),
            "deal_date": cfm.date(self.deal_date),
            "deal_time": cfm.time(self.deal_time),
            "bid_brokerage_fee": self.bid_bro_fee,
            "offer_brokerage_fee": self.offer_bro_fee,
            "bid_switch": self.bid_switch,
            "offer_switch": self.offer_switch,
            "trade_id": self.deal_id,
        }
