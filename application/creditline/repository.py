import os
from typing import List

import constants
from application.creditline import CreditLine
from utils import fileutils

_LINE_TABLE = {}
_TENORS = [
    "spot",
    "on",
    "tn",
    "sn",
    "1w",
    "2w",
    "3w",
    "1m",
    "2m",
    "3m",
    "4m",
    "5m",
    "6m",
    "7m",
    "8m",
    "9m",
    "10m",
    "11m",
    "1y",
    "2y",
    "3y",
    "4y",
    "5y",
    "6y",
    "10y",
]


def load_line_table_csv() -> None:
    file_path = os.path.join(constants.RESOURCE_DIR, "creditline", "line table.csv")
    _LINE_TABLE.update(
        {
            (
                cl.source.upper(),
                cl.destination.upper(),
                cl.product.upper(),
                cl.tenor.upper(),
            ): cl
            for row in fileutils.read_csv_to_dicts(file_path)
            for cl in _line_table_row_to_credit_lines(row)
        }
    )


def _line_table_row_to_credit_lines(row: dict) -> List[CreditLine]:
    source = row.get("from")
    destination = row.get("to")
    allows_switch = row.get("allows_switch")
    can_switch = row.get("can_switch")
    return [
        CreditLine(
            source=source,
            destination=destination,
            product="swap",
            tenor=tenor,
            symbol=row.get(tenor, "X"),
            can_switch=can_switch,
            allows_switch=allows_switch,
        )
        for tenor in _TENORS
    ]


def get_credit_line(
    source: str, destination: str, product: str, tenor: str
) -> CreditLine:
    return _LINE_TABLE.get(
        (source.upper(), destination.upper(), product.upper(), tenor.upper())
    )


if not _LINE_TABLE:
    load_line_table_csv()
