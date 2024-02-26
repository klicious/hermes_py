from .fee import Fee
from .repository import get_name_to_fee


def get_fee(house: str) -> Fee:
    name_to_fee = get_name_to_fee()
    return name_to_fee.get(house.upper(), default_fee())


def default_fee() -> Fee:
    return Fee("DEFAULT", "KRW", 6_000)
