from datetime import date

from application import swap


def test_ndf_date_conversion():
    dates = [date(2024, 3, 4), date(2024, 2, 29), date(2024, 2, 28)]
    result = swap.vfm_dates(dates)
    assert result == "4 Mar / 29.28 Feb 24"

    dates = [date(2023, 12, 31), date(2024, 1, 1), date(2024, 1, 2)]
    result = swap.vfm_dates(dates)
    assert result == "2.1 Jan 24 / 31 Dec 23"
