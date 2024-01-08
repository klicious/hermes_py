from dataclasses import dataclass, field
from datetime import date, datetime

from utils import dateutils


@dataclass
class Trade:
    trade_date: date
    bid: str
    offer: str
    price: float  # Using float for currency representation
    amount: int
    rate: float
    value_date: date
    mar: float
    bid_brokerage_fee: float
    offer_brokerage_fee: float
    deal_time: datetime
    swap: bool
    trader: str = field(default=None)
    bid_their_to: str = field(default=None)
    offer_their_to: str = field(default=None)
    product: str = field(default="spotmar")
    spot_date: date = field(init=False)

    def __post_init__(self):
        self.spot_date = dateutils.add_workdays(self.trade_date, 2)

    def cfm_dict(self, entity) -> dict:
        if entity == self.bid:
            deal = "buy"
            direction = "from"
        else:
            deal = "sell"
            direction = "to"
        return {
            "trade_date": self.trade_date.isoformat(),
            "bid": self.bid,
            "offer": self.offer,
            "price": str(round(self.price, 2)),
            "amount": str(round(self.amount, 2)),
            "rate": str(round(self.rate, 2)),
            "value_date": self.value_date.isoformat(),
            "mar": str(round(self.mar, 2)),
            "bid_brokerage_fee": str(round(self.bid_brokerage_fee)),
            "offer_brokerage_fee": str(round(self.offer_brokerage_fee)),
            "deal_time": self.deal_time.isoformat(),
            "swap": str(self.swap),
            "trader": self.trader,
            "bid_their_to": self.bid_their_to,
            "offer_their_to": self.offer_their_to,
            "product": self.product,
            "spot_date": self.spot_date.isoformat(),
            "deal": deal,
            "direction": direction,
        }
