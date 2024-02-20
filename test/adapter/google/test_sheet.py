from adapter.google import sheet


def test_sheet():
    values = sheet.get_values("houses", "A:F")
    print(values)
