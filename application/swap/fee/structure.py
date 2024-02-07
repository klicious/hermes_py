import operator
import re
from dataclasses import dataclass
from typing import List, Tuple, Callable

from .. import tenor as tnr

OPERATORS = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
}

BOUNDARY_PATTERN = re.compile(r"([<>]=?)(\d+\w)")


@dataclass
class FeeStructure:
    rates: List[int]
    currency: str
    boundaries: List[str]
    operators: List[Callable]
    first_range_max: int

    @staticmethod
    def of(rates: List[int], currency: str, boundaries: List[str]):
        """
        :param rates: list of rates with length of boundaries list + 1
        :param currency: krw, usd, eur, jpy, etc
        :param boundaries: e.g. ["<1w", "<1m", "<=1y"]
        :return:
        """
        assert len(rates) == len(boundaries) + 1
        bds, operators = parse_boundaries(boundaries)
        return FeeStructure(rates, currency, bds, operators)

    def calculate_fee(self, tenor: str, days: int) -> Tuple[int, str]:
        tnr_d = tnr.to_days(tenor)
        for boundary, rate, op in zip(self.boundaries, self.rates, self.operators):
            boundary_days = tnr.to_days(boundary)
            if op(tnr_d, boundary_days):
                fee = rate * days
                return (
                    (min(fee, self.first_range_max), self.currency)
                    if rate == self.rates[0]
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
        parsed_boundaries.append(tenor)
        parsed_operators.append(OPERATORS[op_symbol])

    return parsed_boundaries, parsed_operators
