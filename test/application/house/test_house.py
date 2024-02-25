from application import house


def test_get_houses():
    banks = house.get_name_to_house()
    assert len(banks) > 0
    print(banks)
