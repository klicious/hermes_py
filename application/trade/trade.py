from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import Protocol

from utils import stringutils
from . import confirmation as cfm


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
    deal_id: str = field(default_factory=stringutils.generate_uuid)

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

    def brokerage_fee(self, entity: str):
        if entity == self.bid:
            return self.bid_bro_fee
        if entity == self.offer:
            return self.offer_bro_fee
        return 0

    def has_entity(self, entity) -> bool:
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
            "product": self.product,
            "bid": self.bid,
            "offer": self.offer,
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
