from datetime import date, datetime

from application.spotmar import Trade, by_entity_rate, reuter

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


def test_by_entity_rate():
    grouped_trades = by_entity_rate(TRADES)
    print(grouped_trades)


def test_reuter_messages():
    messages = reuter(TRADES)
    print(messages)
