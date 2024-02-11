from application import house


def test_get_banks():
    banks = house.get_houses()
    assert len(banks) > 0
    print(banks)
