from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Dict, Tuple

import constants
from utils import fileutils
from .structure import FeeStructure

_NAME_TO_FEE_RATE: Dict[Tuple[str, str], Fee] = {}
HOUSE_TO_FEE_STRUCTURE: Dict[Tuple[str, str], FeeStructure] = {}


def _load_swap_fee_csv() -> None:
    file_path = os.path.join(constants.RESOURCE_DIR, "swap", "fee.csv")
    _NAME_TO_FEE_RATE.update(
        {
            (row.get("house"), row.get("product")): fee
            for row in fileutils.read_csv_to_dicts(file_path)
            for fee in _row_to_fees(row)
            if row.get("product")
        }
    )


def _row_to_fees(row) -> List[Fee]:
    house = row.get("house").upper() if "house" in row else ""
    product = row.get("product").upper() if "product" in row else ""
    currency = row.get("currency").upper() if "currency" in row else ""
    fpm = row.get("fpm").upper() if "fpm" in row else ""
    mp1 = row.get("mp1").upper() if "mp1" in row else ""
    ppd1 = row.get("ppd1").upper() if "ppd1" in row else ""
    b1 = row.get("b1").upper() if "b1" in row else ""
    ppd2 = row.get("ppd2").upper() if "ppd2" in row else ""
    b2 = row.get("b2").upper() if "b2" in row else ""
    ppd3 = row.get("ppd3").upper() if "ppd3" in row else ""
    b3 = row.get("b3").upper() if "b3" in row else ""
    ppd4 = row.get("ppd4").upper() if "ppd4" in row else ""
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
        _load_swap_fee_csv()


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
