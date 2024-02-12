from __future__ import annotations

from typing import Tuple, Dict

from .structure import FeeStructure

HOUSE_CONFIGS: Dict[str, FeeStructure] = {
    "woori sl": FeeStructure.of(
        product="swap-df",
        rates=[1_000, 5_000, 15_000, 20_000],
        first_range_max=5_000,
        currency="KRW",
        boundaries=["<1w", "<1m", "<=1y"],
    ),
    "kookmin sl": FeeStructure.of(
        product="swap-ndf",
        rates=[1, 5, 15, 20],
        currency="KRW",
        boundaries=["<1w", "<1m", "<=1y"],
        fixed_rate=15_000,
    ),
    "default": FeeStructure.of(
        product="swap",
        rates=[1, 5, 15, 20],
        currency="USD",
        boundaries=["<1w", "<1m", "<=1y"],
    ),
    # Add more houses as needed
}


def get_fee(house: str, tenor: str, days: int) -> Tuple[int, str]:
    fee_structure = HOUSE_CONFIGS.get(house, HOUSE_CONFIGS["default"])
    return fee_structure.calculate_fee(tenor, days)
