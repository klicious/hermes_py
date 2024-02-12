import os

import constants
from application.spotmar.fee.fee import Fee
from utils import fileutils

_NAME_TO_FEE = {}


def load_spotmar_fee_csv() -> None:
    file_path = os.path.join(constants.RESOURCE_DIR, "spotmar", "fee.csv")
    _NAME_TO_FEE.update(
        {
            row.get("house"): row_to_fee(row)
            for row in fileutils.read_csv_to_dicts(file_path)
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
    load_spotmar_fee_csv()
