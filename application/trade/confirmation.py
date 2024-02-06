from datetime import date, datetime, time
from typing import Tuple


def date(d: date) -> str:
    return d.isoformat()


def datetime(dt: datetime) -> str:
    return dt.isoformat()


def time(t: time) -> str:
    return t.isoformat()


def rate(r: float) -> str:
    return str(round(r, 2))


def action(entity: str, bid: str, offer: str) -> Tuple[str, str, str]:
    if entity != bid and entity != offer:
        raise ValueError(entity, bid, offer)
    return ("buy", "from", offer) if entity == bid else ("sell", "to", bid)
