from __future__ import annotations

from typing import Tuple, Dict

from .structure import FeeStructure

HOUSE_CONFIGS: Dict[str, FeeStructure] = {
    "woori sl": FeeStructure.of(
        rates=[1, 5, 15, 20],
        currency="KRW",
        boundaries=["<1w", "<1m", "<=1y"],
    ),
    "default": FeeStructure(
        rates=[1, 5, 15, 20],
        currency="USD",
        boundaries=["<1w", "<1m", "<=1y"],
    ),
    # Add more houses as needed
}


def get_fee(house: str, tenor: str, days: int) -> Tuple[int, str]:
    fee_structure = HOUSE_CONFIGS.get(house, HOUSE_CONFIGS["default"])
    return fee_structure.calculate_fee(tenor, days)
