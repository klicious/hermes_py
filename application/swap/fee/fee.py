from __future__ import annotations

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


def calculate_fee(house: str, product: str, tenor: str, days: int) -> Tuple[int, str]:
    name_to_fee_structure = get_name_to_fee_structure()
    fee_structure = name_to_fee_structure.get((house, product), DEFAULT_FEE_STRUCTURE)
    return fee_structure.calculate_fee(tenor, days)
