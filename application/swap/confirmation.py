from collections import defaultdict
from datetime import date as date_o, datetime as datetime_o, time as time_o
from typing import Tuple, List

from utils import numberutils


def date(d: date_o) -> str:
    return d.strftime("%d%b%y")


def datetime(dt: datetime_o) -> str:
    return dt.isoformat()


def time(t: time_o) -> str:
    return t.strftime("%H%M")


def rate(r: float) -> str:
    return f"{r:.3f}"


def amount(amt: float) -> str:
    return str(round(amt))


def action(entity: str, bid: str, offer: str) -> Tuple[str, str, str]:
    if entity != bid and entity != offer:
        raise ValueError(entity, bid, offer)
    return ("buy", "b/s", offer) if entity == bid else ("sell", "s/b", bid)


def bro_fee(fee: float, currency: str = "krw"):
    return (
        f"bro {currency} {numberutils.accounting_format(fee)}"
        if fee
        else "no brokerage"
    )


def vfm_dates(dates: List[date_o]) -> str:
    # Group dates by year, then by month
    date_groups = defaultdict(lambda: defaultdict(list))
    for dt in dates:
        date_groups[dt.year][dt.month].append(dt.day)

    formatted_groups = []
    for year, months in sorted(
        date_groups.items(), reverse=True
    ):  # Sort years in reverse
        month_groups = []
        for month, days in sorted(
            months.items(), reverse=True
        ):  # Sort months in reverse
            month_str = date_o(year, month, 1).strftime("%b")
            days_str = ".".join(
                map(str, sorted(days, reverse=True))
            )  # Sort days in reverse
            month_groups.append(f"{days_str} {month_str}")
        # Append the year to the last month group of the year
        month_groups[-1] = f"{month_groups[-1]} {str(year)[2:]}"
        # Add the formatted month groups to the overall list, reversing the order to get earlier months first
        formatted_groups.extend(month_groups)

    return " / ".join(formatted_groups)
