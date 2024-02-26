from adapter.google import sheets


def test_sheet():
    values = sheets.get_values("houses", "A:F")
    print(values)
