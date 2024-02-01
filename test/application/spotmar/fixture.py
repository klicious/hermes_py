from datetime import date, datetime

from application.spotmar import Trade

TRADES = [
    Trade(
        trade_date=date.today(),
        bid="shinhan",
        offer="jpmc",
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
        bid="morgan",
        offer="shinhan",
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
        bid="citi",
        offer="shinhan",
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
        bid="shinhan",
        offer="morgan",
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
        bid="jpmc",
        offer="citi",
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
