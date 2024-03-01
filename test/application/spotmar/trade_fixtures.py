from datetime import date, datetime

from application.spotmar import Deal

TRADES = [
    Deal(
        trade_date=date.today(),
        bid_house="shinhan sl",
        offer_house="jpmc sl",
        price=1300.5,
        amount=100,
        rate=5,
        value_date=date.today(),
        mar=1300,
        bid_brokerage_fee=600_000,
        offer_brokerage_fee=600_000,
        deal_time=datetime.now(),
    ),
    Deal(
        trade_date=date.today(),
        bid_house="citi sl",
        offer_house="morgan sl",
        price=1300,
        amount=50,
        rate=0,
        value_date=date.today(),
        mar=1300,
        bid_brokerage_fee=300_000,
        offer_brokerage_fee=300_000,
        deal_time=datetime.now(),
    ),
    Deal(
        trade_date=date.today(),
        bid_house="morgan sl",
        offer_house="shinhan sl",
        price=1299.5,
        amount=100,
        rate=-5,
        value_date=date.today(),
        mar=1300,
        bid_brokerage_fee=600_000,
        offer_brokerage_fee=600_000,
        deal_time=datetime.now(),
    ),
    Deal(
        trade_date=date.today(),
        bid_house="jpmc sl",
        offer_house="citi sl",
        price=1300,
        amount=100,
        rate=0,
        value_date=date.today(),
        mar=1300,
        bid_brokerage_fee=600_000,
        offer_brokerage_fee=600_000,
        deal_time=datetime.now(),
    ),
    Deal(
        trade_date=date.today(),
        bid_house="shinhan sl",
        offer_house="anz sl",
        price=1300.5,
        amount=500,
        rate=5,
        value_date=date.today(),
        mar=1300,
        bid_brokerage_fee=600_000,
        offer_brokerage_fee=600_000,
        deal_time=datetime.now(),
        bid_switch=True,
    ),
    Deal(
        trade_date=date.today(),
        bid_house="kb sl",
        offer_house="shinhan sl",
        price=1300.5,
        amount=500,
        rate=5,
        value_date=date.today(),
        mar=1300,
        bid_brokerage_fee=600_000,
        offer_brokerage_fee=600_000,
        deal_time=datetime.now(),
        offer_switch=True,
    ),
]
