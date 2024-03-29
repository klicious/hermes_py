from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Dict, Tuple

from more_itertools import consume

import constants
from adapter.google import sheets
from utils import fileutils
from .structure import FeeStructure

_NAME_TO_FEE_RATE: Dict[Tuple[str, str], Fee] = {}
HOUSE_TO_FEE_STRUCTURE: Dict[Tuple[str, str], FeeStructure] = {}

SWAP_DF = "df"
SWAP_NDF = "nd"
_products = [SWAP_DF, SWAP_NDF]


def _load_swap_fee_csv() -> None:
    file_path = os.path.join(constants.RESOURCE_DIR, "swap", "fee.csv")
    _NAME_TO_FEE_RATE.update(
        {
            (fee.house, fee.product): fee
            for row in fileutils.read_csv_to_dicts(file_path)
            for fee in _row_to_fees(row)
            if row.get("product")
        }
    )


def __load_fee_from_google_sheet(product: str) -> None:
    _NAME_TO_FEE_RATE.update(
        {
            (fee.house, fee.product): fee
            for row in sheets.get_values(f"{product} fees", "A:M")
            for fee in _row_to_fees(row)
            if row.get("currency")
        }
    )


def _row_to_fees(row) -> List[Fee]:
    house = row.get("house").upper()
    product = row.get("product", "").upper()
    currency = row.get("currency", "").upper()
    fpm = row.get("fpm", "").upper()
    mp1 = row.get("mp1", "").upper()
    ppd1 = row.get("ppd1", "").upper()
    b1 = row.get("b1", "").upper()
    ppd2 = row.get("ppd2", "").upper()
    b2 = row.get("b2", "").upper()
    ppd3 = row.get("ppd3", "").upper()
    b3 = row.get("b3", "").upper()
    ppd4 = row.get("ppd4", "").upper()
    return (
        [
            Fee(
                house=house,
                product="df",
                currency=currency,
                fpm=fpm,
                mp1=mp1,
                ppd1=ppd1,
                b1=b1,
                ppd2=ppd2,
                b2=b2,
                ppd3=ppd3,
                b3=b3,
                ppd4=ppd4,
            ),
            Fee(
                house=house,
                product="ndf",
                currency=currency,
                fpm=fpm,
                mp1=mp1,
                ppd1=ppd1,
                b1=b1,
                ppd2=ppd2,
                b2=b2,
                ppd3=ppd3,
                b3=b3,
                ppd4=ppd4,
            ),
        ]
        if product == "swap"
        else [
            Fee(
                house=house,
                product=product,
                currency=currency,
                fpm=fpm,
                mp1=mp1,
                ppd1=ppd1,
                b1=b1,
                ppd2=ppd2,
                b2=b2,
                ppd3=ppd3,
                b3=b3,
                ppd4=ppd4,
            )
        ]
    )


@dataclass
class Fee:
    house: str
    product: str
    currency: str
    fpm: int
    mp1: int
    ppd1: int
    b1: str
    ppd2: int
    b2: str
    ppd3: int
    b3: str
    ppd4: int

    def to_fee_structure(self) -> FeeStructure:
        rates = [self.ppd1, self.ppd2, self.ppd3, self.ppd4] if self.ppd1 else []
        boundaries = [self.b1, self.b2, self.b3] if self.b1 else []
        return FeeStructure.of(
            house=self.house,
            product=self.product,
            rates=rates,
            currency=self.currency,
            boundaries=boundaries,
            first_range_max=self.fpm,
            fixed_rate=self.mp1,
        )


def init_fee_rate() -> None:
    if not _NAME_TO_FEE_RATE:
        consume(__load_fee_from_google_sheet(p) for p in _products)


def init_house_to_fee_structure() -> None:
    if not HOUSE_TO_FEE_STRUCTURE:
        name_to_fee_rate = get_name_to_fee_rate()
        HOUSE_TO_FEE_STRUCTURE.update(
            {
                (r.house, r.product): r.to_fee_structure()
                for r in name_to_fee_rate.values()
            }
        )


def get_name_to_fee_rate() -> Dict[Tuple[str, str], Fee]:
    init_fee_rate()
    return _NAME_TO_FEE_RATE


def get_fee_rate(house: str, product: str) -> Fee:
    init_fee_rate()
    return _NAME_TO_FEE_RATE.get(
        (house.upper(), product.upper()), _default_fee_rate(product)
    )


def _default_fee_rate(product: str) -> Fee:
    return (
        Fee(
            house="default",
            product="DF",
            currency="KRW",
            fpm=0,
            mp1=5_000,
            ppd1=1_000,
            b1="1w",
            ppd2=5_000,
            b2="1m",
            ppd3=10_000,
            b3="2m",
            ppd4=15_000,
        )
        if product.upper() == "DF"
        else Fee(
            house="default",
            product="ND",
            currency="KRW",
            fpm=0,
            mp1=5_000,
            ppd1=1_000,
            b1="1w",
            ppd2=5_000,
            b2="1m",
            ppd3=10_000,
            b3="2m",
            ppd4=15_000,
        )
    )


def get_name_to_fee_structure() -> Dict[Tuple[str, str], FeeStructure]:
    init_house_to_fee_structure()
    return HOUSE_TO_FEE_STRUCTURE


init_fee_rate()
