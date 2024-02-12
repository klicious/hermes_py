from application import house


def test_get_banks():
    banks = house.get_name_to_house()
    assert len(banks) > 0
    print(banks)


def test_load_houses_csv():
    house.load_houses_csv()
