import calendar
import csv
import os.path
from datetime import datetime, date, timedelta

from more_itertools import consume

import constants

_HOLIDAYS = {}
_COUNTRY_CODES = ["kr", "us"]


def init():
    if len(_HOLIDAYS) == 0:
        _load_all_holidays()


def end_of_month(
    input_date, working_day: bool = False, country_code: str = None
) -> date:
    # Extract the year and month from the input date
    year, month = input_date.year, input_date.month

    # Find the last day of the month
    last_day = calendar.monthrange(year, month)[1]

    # Return the end of the month date
    eom = date(year, month, last_day)
    return (
        add_workdays(eom, -1)
        if working_day and not is_working_day(eom, country_code)
        else eom
    )


def is_end_of_month(input_date, working_day: bool = False, country_code: str = None):
    # Check if the input date is the last day of the month
    return input_date == end_of_month(input_date, working_day, country_code)


def add_workdays(d: date, n: int, country_code: str = None) -> date:
    step = 1 if n >= 0 else -1
    while n != 0:
        d += timedelta(days=step)
        if is_working_day(d, country_code):
            n -= step

    return d


def is_working_day(d: date, country_code: str = None) -> bool:
    return is_weekday(d) and not is_holiday(d, country_code)


def is_weekday(d: date):
    return d.weekday() < 5


def is_holiday(d: date, country_code: str = None):
    if country_code:
        return d in _HOLIDAYS[country_code.lower()]
    return any(d in holidays for holidays in _HOLIDAYS.values())


def get_holidays(country_code: str):
    if not country_code:
        return _HOLIDAYS
    return _HOLIDAYS[country_code.lower()]


def _load_all_holidays():
    consume(_load_holidays(c) for c in _COUNTRY_CODES)


def _load_holidays(country_code: str):
    """
    :param country_code: 2-letter country code
    :return:
    """
    country_key = country_code.lower()
    holidays = _csv_to_date_dict(country_key)
    _HOLIDAYS[country_key] = holidays


def _csv_to_date_dict(filename):
    """
    :param filename: under the `resources/input`
    :return:
    """
    path = os.path.join(constants.RESOURCE_DIR, "holidays", f"{filename}.csv")
    date_dict = {}

    with open(path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert the date string to a datetime.date object
            date = datetime.strptime(row["date"], "%Y-%m-%d").date()
            # Assign the date object as key and name as value
            date_dict[date] = row["name"]

    return date_dict


init()
