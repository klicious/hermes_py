from __future__ import annotations

from datetime import date
from typing import Tuple

from .repository import get_name_to_fee_structure
from .structure import FeeStructure

DEFAULT_FEE_STRUCTURE = FeeStructure.of(
    house="default",
    product="SWAP",
    rates=[1, 5, 15, 20],
    currency="USD",
    boundaries=["<1w", "<1m", "<=1y"],
)


def calculate_fee(
    house: str, product: str, tenor: str, trade_date: date
) -> Tuple[int, str]:
    name_to_fee_structure = get_name_to_fee_structure()
    fee_structure = name_to_fee_structure.get(
        (house.upper(), product.upper()), DEFAULT_FEE_STRUCTURE
    )
    return fee_structure.calculate_fee(tenor, trade_date)
