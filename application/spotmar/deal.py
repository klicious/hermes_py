from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List

from adapter.google import sheets
from utils import dateutils, stringutils
from . import confirmation as cfm
from . import fee
from ..trade import tenor


def cfm_date(d: date) -> str:
    return d.isoformat()


def cfm_datetime(dt: datetime) -> str:
    return dt.isoformat()


@dataclass
class Deal:
    trade_date: date
    bid_house: str
    offer_house: str
    price: float
    amount: int
    rate: float
    value_date: date
    mar: float
    bid_brokerage_currency: str
    bid_brokerage_fee: int
    offer_brokerage_currency: str
    offer_brokerage_fee: int
    deal_time: datetime
    bid_switch: bool = field(default=False)
    offer_switch: bool = field(default=False)
    bid_trader: str = field(default="")
    offer_trader: str = field(default="")
    bid_their_to: str = field(default="")
    offer_their_to: str = field(default="")
    product: str = field(default="spotmar")
    deal_id: str = field(default_factory=stringutils.generate_uuid)
    spot_date: date = field(init=False)

    def __post_init__(self):
        self.spot_date = dateutils.add_workdays(self.trade_date, 2)
        self.bid_house = self.bid_house.strip().upper()
        self.offer_house = self.offer_house.strip().upper()
        self.bid_trader = self.bid_trader.strip().upper() if self.bid_trader else ""
        self.offer_trader = (
            self.offer_trader.strip().upper() if self.offer_trader else ""
        )
        self.bid_their_to = (
            self.bid_their_to.strip().upper() if self.bid_their_to else ""
        )
        self.offer_their_to = (
            self.offer_their_to.strip().upper() if self.offer_their_to else ""
        )
        self.product = self.product.strip().upper()

    @staticmethod
    def of(
        trade_date: date,
        bid: str,
        offer: str,
        price: int,
        amount: int,
        rate: float,
        mar: float,
        deal_time: datetime,
        switch: str,
        bid_trader: str,
        offer_trader: str,
        bid_their_to: str,
        offer_their_to: str,
    ):
        bid_house = stringutils.get_trader(bid).get("symbol", "")
        offer_house = stringutils.get_trader(offer).get("symbol", "")
        trade_date = deal_time.date()
        bid_switch = True if switch.upper() == "BID" else False
        offer_switch = True if switch.upper() == "OFFER" else False
        bid_brokerage_fee: fee.Fee = fee.get_fee(bid_house)
        offer_brokerage_fee: fee.Fee = fee.get_fee(offer_house)
        bid_brokerage_amount = 0 if bid_switch else bid_brokerage_fee.sum(amount)
        offer_brokerage_amount = 0 if offer_switch else offer_brokerage_fee.sum(amount)
        value_date = tenor.spot(trade_date)
        return Deal(
            trade_date=trade_date,
            bid_house=bid_house,
            offer_house=offer_house,
            price=price,
            amount=amount,
            rate=rate,
            value_date=value_date,
            mar=mar,
            bid_brokerage_currency=bid_brokerage_fee.currency,
            bid_brokerage_fee=bid_brokerage_amount,
            offer_brokerage_currency=offer_brokerage_fee.currency,
            offer_brokerage_fee=offer_brokerage_amount,
            deal_time=deal_time,
            bid_switch=bid_switch,
            offer_switch=offer_switch,
            bid_trader=bid_trader,
            offer_trader=offer_trader,
            bid_their_to=bid_their_to,
            offer_their_to=offer_their_to,
            product="spotmar",
        )

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
        h = house.upper()
        return self.bid_house == h or self.offer_house == h

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
            "bid_brokerage_currency": self.bid_brokerage_currency,
            "bid_brokerage_fee": cfm.amount(self.bid_bro_fee),
            "offer_brokerage_currency": self.offer_brokerage_currency,
            "offer_brokerage_fee": cfm.amount(self.offer_bro_fee),
            "deal_time": cfm_datetime(self.deal_time),
            "bid_switch": self.bid_switch,
            "offer_switch": self.offer_switch,
            "trader": self.trader,
            "bid_their_to": self.bid_their_to,
            "offer_their_to": self.offer_their_to,
            "spot_date": cfm_date(self.spot_date),
        }


def get_deals() -> List[Deal]:
    return [
        Deal.of(
            trade_date=date.fromisoformat(d.get("DPRH")),
            bid=d.get("BID"),
            offer=d.get("OFFER"),
            price=d.get("PX"),
            amount=d.get("Q"),
            rate=d.get("RATE"),
            mar=d.get("M.A.R"),
            deal_time=d.get("TIME"),
            switch=d.get("SWITCH"),
            bid_trader=d.get("TRADER_B"),
            offer_trader=d.get("TRADER_O", ""),
            bid_their_to=d.get("BID THEIR TO", ""),
            offer_their_to=d.get("OFFER THEIR TO"),
        )
        for d in sheets.get_values("spotmar daily", "A:Q")
    ]


def get_all_deals():
    pass
