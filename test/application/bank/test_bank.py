from application import bank


def test_get_banks():
    banks = bank.get_banks()
    assert len(banks) > 0
    print(banks)
