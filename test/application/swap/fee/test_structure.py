from application.swap import fee


def test_calculate_fee():
    house = "default"
    bro_fee, currency = fee.get_fee(house, "1m", 1)
    assert bro_fee == 15
    assert currency == "USD"
    bro_fee, currency = fee.get_fee(house, "2w", 1)
    assert bro_fee == 5
    assert currency == "USD"
    bro_fee, currency = fee.get_fee(house, "5d", 1)
    assert bro_fee == 1
    assert currency == "USD"
    bro_fee, currency = fee.get_fee(house, "1y", 1)
    assert bro_fee == 15
    assert currency == "USD"
    bro_fee, currency = fee.get_fee(house, "2y", 1)
    assert bro_fee == 20
    assert currency == "USD"

    house = "woori sl"
    bro_fee, currency = fee.get_fee(house, "6d", 1)
    assert bro_fee == 1_000
    assert currency == "KRW"
    bro_fee, currency = fee.get_fee(house, "5d", 1)
    assert bro_fee == 1_000
    assert currency == "KRW"
    bro_fee, currency = fee.get_fee(house, "6d", 5)
    assert bro_fee == 5_000
    assert currency == "KRW"
    bro_fee, currency = fee.get_fee(house, "5d", 5)
    assert bro_fee == 5_000
    assert currency == "KRW"
    bro_fee, currency = fee.get_fee(house, "6d", 6)
    assert bro_fee == 5_000
    assert currency == "KRW"
    bro_fee, currency = fee.get_fee(house, "5d", 6)
    assert bro_fee == 5_000
    assert currency == "KRW"
