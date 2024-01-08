from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Tuple, Callable

from dateutil.relativedelta import relativedelta

from utils import dateutils


def overnight(_trade: date) -> date:
    return dateutils.add_workdays(_trade, 1)


def spot(_trade: date) -> date:
    return dateutils.add_workdays(_trade, 2)


def fixing(_value: date) -> date:
    return dateutils.add_workdays(_value, -1, "kr")


def mar(_fixing: date) -> date:
    return dateutils.add_workdays(_fixing, -1, "kr")


def week(_spot: date, n: int = 1) -> date:
    v = _spot + timedelta(weeks=n)
    if dateutils.is_holiday(v):
        return dateutils.add_workdays(v, -1)
    return v


def month(_spot: date, n: int = 1, end_of_month: bool = False) -> date:
    v = _spot + relativedelta(months=n)
    if end_of_month:
        return dateutils.end_of_month(v, working_day=True)
    if not dateutils.is_working_day(v):
        return dateutils.add_workdays(v, 1)
    return v


def year(_spot: date, n: int = 1, end_of_month: bool = False) -> date:
    v = _spot + relativedelta(years=n)
    if end_of_month:
        return dateutils.end_of_month(v, working_day=True)
    if not dateutils.is_working_day(v):
        return dateutils.add_workdays(v, 1)
    return v


def _separate_numeric(string):
    match = re.match(r"(\d*)(\D+)", string)
    if match:
        # Extract the numeric part and the string part
        num_part, str_part = match.groups()
        num = int(num_part) if num_part else 0
        return num, str_part
    return 0, string


@dataclass
class Tenor:
    symbol: str
    trade: date
    spot: date = field(init=False)
    _legs: Tuple[Leg, Leg] = field(default=tuple)
    _value_eom: bool = field(init=False)  # value date should be end of month

    def __post_init__(self):
        self.spot = spot(self.trade)
        self._value_eom = dateutils.is_end_of_month(month(self.spot), working_day=True)
        self._init_legs()
        self._func(self.symbol)

    def _init_legs(self):
        first, second = self.near_far_symbols
        n, near_tenor = _separate_numeric(first)
        tenor_func = self._func(near_tenor)
        first_near_date, first_value_date = tenor_func(n=n)
        n, far_tenor = _separate_numeric(second)
        tenor_func = self._func(far_tenor)
        near_date, second_value_date = tenor_func(
            n=n, near_date=first_value_date if first_value_date else first_near_date
        )
        self._legs = self._make_legs(
            near_tenor, near_date, far_tenor, second_value_date
        )

    @property
    def near_far_symbols(self) -> Tuple[str, str]:
        symbols = self.symbol.split("*")
        near = ""
        far = self.symbol
        if len(symbols) == 2:
            near = symbols[0].strip()
            far = symbols[1].strip()
        return near, far

    @property
    def near(self) -> Leg:
        return self._legs[0]

    @property
    def far(self) -> Leg:
        return self._legs[1]

    @property
    def near_date(self) -> date:
        return self.near.value

    @property
    def far_date(self) -> date:
        return self.far.value

    @property
    def fixing_date(self) -> date:
        return self.far.fixing

    @property
    def mar_date(self) -> date:
        return self.far.mar

    def _func(self, tenor: str) -> Callable:
        _functions = {
            "spot": self._spot,
            "on": self._overnight,
            "o/n": self._overnight,
            "tn": self._tomorrow_next,
            "t/n": self._tomorrow_next,
            "sn": self._spot_next,
            "s/n": self._spot_next,
            "w": self._week,
            "wk": self._week,
            "m": self._month,
            "y": self._year,
        }
        return _functions.get(tenor, self._default)

    def _default(self, **kwargs):
        return None, None

    def _spot(self, **kwargs):
        return self.trade, self.spot

    def _overnight(self, **kwargs) -> Tuple[date, date]:
        near_date = self.trade
        far_date = overnight(near_date)
        return near_date, far_date

    def _tomorrow_next(self, **kwargs) -> Tuple[date, date]:
        near_date = overnight(self.trade)
        far_date = overnight(near_date)
        return near_date, far_date

    def _spot_next(self, **kwargs) -> Tuple[date, date]:
        near_date = self.spot
        far_date = overnight(near_date)
        return near_date, far_date

    def _week(self, **kwargs) -> Tuple[date, date]:
        """
        :param kwargs:
            n = # of weeks
            near_date = near date. defaults to spot date
        :return:
        """
        n = kwargs.get("n", 1)
        near_date = kwargs.get("near_date")
        if near_date is None:
            near_date = self.spot
        far_date = week(near_date, n)
        return near_date, far_date

    def _month(self, **kwargs) -> Tuple[date, date]:
        """
        :param kwargs:
            n = # of months
            near_date = near date. defaults to spot date
        :return:
        """
        n = kwargs.get("n", 1)
        near_date = kwargs.get("near_date")
        if near_date is None:
            near_date = self.spot
        far_date = month(near_date, n, self._value_eom)
        return near_date, far_date

    def _year(self, **kwargs) -> Tuple[date, date]:
        """
        :param kwargs:
            n = # of years
            near_date = near date. defaults to spot date
        :return:
        """
        n = kwargs.get("n", 1)
        near_date = kwargs.get("near_date")
        if near_date is None:
            near_date = self.spot
        far_date = year(near_date, n, self._value_eom)
        return near_date, far_date

    def _make_legs(self, near_tenor: str, near: date, far_tenor: str, far: date):
        return Leg(near_tenor, self.trade, near), Leg(far_tenor, self.trade, far)


@dataclass
class Leg:
    symbol: str
    trade: date
    value: date
    fixing: date = field(init=False)
    mar: date = field(init=False)

    def __post_init__(self):
        self.fixing = fixing(self.value)
        self.mar = mar(self.fixing)
