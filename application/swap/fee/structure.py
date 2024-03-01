import operator
import re
from dataclasses import dataclass, field
from datetime import date
from typing import List, Tuple, Callable

from ...trade import tenor as tnr

OPERATORS = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
}

BOUNDARY_PATTERN = re.compile(r"([<>]=?)(\d+\w)")


@dataclass
class FeeStructure:
    house: str
    product: str
    rates: List[int]
    currency: str
    boundaries: List[str]
    operators: List[Callable]
    first_range_max: int = field(default=None)
    fixed_rate: int = field(default=None)

    @staticmethod
    def of(
        house: str,
        product: str,
        rates: List[int],
        currency: str,
        boundaries: List[str],
        first_range_max: int = None,
        fixed_rate: int = None,
    ):
        """
        :param rates: list of rates with length of boundaries list + 1
        :param currency: krw, usd, eur, jpy, etc...
        :param boundaries: e.g. ["<1w", "<1m", "<=1y"]
        :param first_range_max: if the first range has a capped value
        :param fixed_rate: when the rate is fixed regardless of the tenor
        :return:
        """
        if rates and boundaries:
            assert len(rates) == len(boundaries) + 1
        bds, operators = parse_boundaries(boundaries)
        return FeeStructure(
            house.upper(),
            product.upper(),
            rates,
            currency.upper(),
            bds,
            operators,
            first_range_max=first_range_max,
            fixed_rate=fixed_rate,
        )

    def calculate_fee(self, tenor: str, trade_date: date) -> Tuple[int, str]:
        if not self.rates and not self.fixed_rate:
            return 0, self.currency
        if self.fixed_rate:
            return self.fixed_rate, self.currency
        tnr_d = tnr.to_days(tenor)
        days = tnr.count_days(tenor, trade_date)
        for boundary, rate, op in zip(self.boundaries, self.rates, self.operators):
            boundary_days = tnr.to_days(boundary)
            if op(tnr_d, boundary_days):
                fee = rate * days
                return (
                    (min(fee, self.first_range_max), self.currency)
                    if rate == self.rates[0] and self.first_range_max
                    else (fee, self.currency)
                )
        return self.rates[-1] * days, self.currency


def parse_boundaries(boundary_strings: List[str]) -> Tuple[List[str], List[Callable]]:
    parsed_boundaries = []
    parsed_operators = []

    for boundary_string in boundary_strings:
        match = BOUNDARY_PATTERN.match(boundary_string)
        if not match:
            raise ValueError(f"Invalid boundary format: {boundary_string}")

        # Extract operator and tenor from the match groups
        op_symbol, tenor = match.groups()
        parsed_boundaries.append(tenor.upper())
        parsed_operators.append(OPERATORS[op_symbol])

    return parsed_boundaries, parsed_operators
