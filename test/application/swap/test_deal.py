from more_itertools import consume

from application.swap import deal


def test_get_deals():
    deals = deal.get_deals()
    print(deals)
    assert 0 < len(deals)
    consume(print(d) for d in deals)
