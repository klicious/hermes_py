from datetime import date, datetime

from application.spotmar import Trade

TRADES = [
    Trade(
        trade_date=date.today(),
        bid_house="shinhan",
        offer_house="jpmc",
        price=1300.5,
        amount=100,
        rate=5,
        value_date=date.today(),
        mar=1300,
        bid_brokerage_fee=600_000,
        offer_brokerage_fee=600_000,
        deal_time=datetime.now(),
    ),
    Trade(
        trade_date=date.today(),
        bid_house="morgan",
        offer_house="shinhan",
        price=1299.5,
        amount=100,
        rate=-5,
        value_date=date.today(),
        mar=1300,
        bid_brokerage_fee=600_000,
        offer_brokerage_fee=600_000,
        deal_time=datetime.now(),
    ),
    Trade(
        trade_date=date.today(),
        bid_house="citi",
        offer_house="shinhan",
        price=1300.5,
        amount=100,
        rate=5,
        value_date=date.today(),
        mar=1300,
        bid_brokerage_fee=600_000,
        offer_brokerage_fee=600_000,
        deal_time=datetime.now(),
        offer_switch=True,
    ),
    Trade(
        trade_date=date.today(),
        bid_house="shinhan",
        offer_house="morgan",
        price=1300.5,
        amount=100,
        rate=5,
        value_date=date.today(),
        mar=1300,
        bid_brokerage_fee=600_000,
        offer_brokerage_fee=600_000,
        deal_time=datetime.now(),
        bid_switch=True,
    ),
    Trade(
        trade_date=date.today(),
        bid_house="jpmc",
        offer_house="citi",
        price=1300,
        amount=100,
        rate=0,
        value_date=date.today(),
        mar=1300,
        bid_brokerage_fee=600_000,
        offer_brokerage_fee=600_000,
        deal_time=datetime.now(),
    ),
]
