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
        swap=False,
    ),
    Trade(
        trade_date=date.today(),
        bid="citi",
        offer="morgan",
        price=1300,
        amount=50,
        rate=0,
        value_date=date.today(),
        mar=1300,
        bid_brokerage_fee=300_000,
        offer_brokerage_fee=300_000,
        deal_time=datetime.now(),
        swap=False,
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
        swap=False,
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
        swap=False,
    ),
]
