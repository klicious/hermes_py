import os

import constants
from adapter.google import sheets
from utils import fileutils
from .fee import Fee

_NAME_TO_FEE = {}


def _load_spotmar_fee_csv() -> None:
    file_path = os.path.join(constants.RESOURCE_DIR, "spotmar", "fee.csv")
    _NAME_TO_FEE.update(
        {
            row.get("house"): row_to_fee(row)
            for row in fileutils.read_csv_to_dicts(file_path)
        }
    )


def _load_spotmar_fee_google_sheet() -> None:
    _NAME_TO_FEE.update(
        {
            row.get("houses").upper(): row_to_fee(row)
            for row in sheets.get_values("spotmar fees", "A:C")
        }
    )


def row_to_fee(row) -> Fee:
    house = row.get("house")
    currency = row.get("currency")
    amount = row.get("amount")
    return Fee(house, currency, amount)


def get_name_to_fee():
    return _NAME_TO_FEE


if not _NAME_TO_FEE:
    _load_spotmar_fee_google_sheet()
