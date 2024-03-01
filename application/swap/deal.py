from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List

from adapter.google import sheets
from application.trade.tenor import Tenor, Leg
from utils import stringutils
from . import confirmation as cfm
from . import fee


@dataclass
class Deal:
    type: str
    trade_date: date
    tenor: str
    bid_house: str
    bid_entity: str
    bid_trader: str
    offer_house: str
    offer_entity: str
    offer_trader: str
    margin: int
    amount: int
    near_rate: float
    far_rate: float
    bid_brokerage_fee: int
    offer_brokerage_fee: int
    confirmation_done: bool = field(default=False)
    deal_time: datetime = field(default_factory=datetime.now)
    bid_switch: bool = field(default=False)
    offer_switch: bool = field(default=False)
    _tenor: Tenor = field(init=False)
    product: str = field(default=None)
    remark: str = field(default="")
    deal_id: str = field(default_factory=stringutils.generate_uuid)

    def __post_init__(self):
        self._tenor = Tenor(self.tenor, self.trade_date)
        self.product = (
            self.product.upper() if self.product else self._tenor.product.upper()
        )
        self.type = self.type.strip().upper()
        self.tenor = self.tenor.strip().upper()
        self.bid_house = self.bid_house.strip().upper()
        self.bid_entity = self.bid_entity.strip().upper()
        self.offer_house = self.offer_house.strip().upper()
        self.offer_entity = self.offer_entity.strip().upper()

    @staticmethod
    def of(
        tenor: str,
        bid_nickname: str,
        offer_nickname: str,
        margin: int,
        amount: int,
        near_rate: float,
        far_rate: float,
        deal_datetime: datetime,
        confirmation_done: bool,
        bid_trader_nickname: str = "",
        offer_trader_nickname: str = "",
        type: str = "df",
        remark: str = "",
        bid_switch: bool = False,
        offer_switch: bool = False,
    ):
        bid_trader = stringutils.get_trader(bid_nickname)
        offer_trader = stringutils.get_trader(offer_nickname)
        trade_date = deal_datetime.date() if deal_datetime else date.today()
        deal_time = deal_datetime if deal_datetime else datetime.now()
        bid_trader_nickname = (
            bid_trader_nickname if bid_trader_nickname else bid_trader.get("trader")
        )
        offer_trader_nickname = (
            offer_trader_nickname
            if offer_trader_nickname
            else offer_trader.get("trader")
        )
        product = type if type else "df"
        bid_house = bid_trader.get("house", "")
        bid_entity = bid_trader.get("entity", "")
        bid_house_symbol = f"{bid_house} {bid_entity}"
        offer_house = offer_trader.get("house", "")
        offer_entity = offer_trader.get("entity", "")
        offer_house_symbol = f"{offer_house} {offer_entity}"
        bid_brokerage_fee = (
            0
            if bid_switch
            else fee.calculate_fee(bid_house_symbol, product, tenor, trade_date)
        )
        offer_brokerage_fee = (
            0
            if offer_switch
            else fee.calculate_fee(offer_house_symbol, product, tenor, trade_date)
        )
        return Deal(
            type=type,
            trade_date=trade_date,
            tenor=tenor,
            bid_house=bid_house,
            bid_entity=bid_entity,
            bid_trader=bid_trader_nickname,
            offer_house=offer_house,
            offer_entity=offer_entity,
            offer_trader=offer_trader_nickname,
            margin=margin,
            amount=amount,
            near_rate=near_rate,
            far_rate=far_rate,
            bid_brokerage_fee=bid_brokerage_fee,
            offer_brokerage_fee=offer_brokerage_fee,
            confirmation_done=confirmation_done,
            deal_time=deal_time,
            bid_switch=bid_switch,
            offer_switch=offer_switch,
            product=product,
            remark=remark,
        )

    @property
    def spot_date(self) -> date:
        return self._tenor.spot

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

    @property
    def delivery(self) -> bool:
        return self.product != "ndf"

    def has_house(self, house: str) -> bool:
        h = house.upper()
        return self.bid_house == h or self.offer_house == h

    def brokerage_fee(self, house):
        if house == self.bid_house:
            return self.bid_bro_fee
        if house == self.offer_house:
            return self.offer_bro_fee
        return 0

    def entity(self, house) -> str:
        if house == self.bid_house:
            return self.bid_entity
        if house == self.offer_house:
            return self.offer_entity
        return ""

    def cfm_dict(self, house) -> dict:
        action, action_pair, counter_party = cfm.action(
            house, self.bid_house, self.offer_house
        )
        brokerage_fee = self.brokerage_fee(house)
        entity = self.entity(house)
        return {
            "trade_date": cfm.date(self.trade_date),
            "tenor": self.tenor,
            "bid": self.bid_house,
            "offer": self.offer_house,
            "house": house,
            "entity": entity,
            "full_house": f"{house} {entity}",
            "counter_party": counter_party,
            "margin": cfm.rate(self.margin),
            "amount": cfm.amount(self.amount),
            "near_rate": cfm.rate(self.near_rate),
            "par_rate": cfm.rate(self.far_rate),
            "bid_brokerage_fee": cfm.amount(self.bid_bro_fee),
            "offer_brokerage_fee": cfm.amount(self.offer_bro_fee),
            "brokerage_fee": cfm.amount(brokerage_fee),
            "deal_date": cfm.date(self.deal_time.date()),
            "deal_datetime": cfm.datetime(self.deal_time),
            "deal_time": cfm.time(self.deal_time.time()),
            "product": self.product,
            "spot_date": cfm.date(self.spot_date),
            "action": action,
            "action_pair": action_pair,
            "near_vfm_dates": cfm.vfm_dates(self._tenor.near.vfm_dates),
            "far_vfm_dates": cfm.vfm_dates(self._tenor.far.vfm_dates),
        }


def get_deals() -> List[Deal]:
    return [
        Deal.of(
            tenor=d.get("TENOR"),
            bid_nickname=d.get("BID", ""),
            offer_nickname=d.get("OFFER", ""),
            margin=d.get("MARGIN"),
            amount=d.get("AMT"),
            near_rate=d.get("NEAR"),
            far_rate=d.get("FAR"),
            deal_datetime=d.get("DEAL_TIME"),
            confirmation_done=True if d.get("CFM") else False,
            bid_trader_nickname=d.get("TRADER_B", ""),
            offer_trader_nickname=d.get("TRADER_O", ""),
            type=d.get("TYPE", "df"),
            remark=d.get("REMARK", ""),
            bid_switch=bool(d.get("SWITCH_B", False)),
            offer_switch=bool(d.get("SWITCH_O", False)),
        )
        for d in sheets.get_values("swap daily", "A:N")
    ]


def get_all_deals():
    pass
