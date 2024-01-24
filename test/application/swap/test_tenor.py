import csv
import time
from datetime import timedelta, date
from typing import List

from dateutil.relativedelta import relativedelta
from more_itertools import consume

from application.swap import Tenor, Leg
from utils import dateutils


def test_tenor_single_leg():
    # trade date 2023-06-28
    trade_date = date(2023, 6, 28)
    symbol = "spot"
    tenor = Tenor(symbol, trade_date)
    # spot
    assert tenor.spot == date(2023, 6, 30)
    ## o/n
    symbol = "o/n"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 28)
    assert tenor.far_date == date(2023, 6, 29)
    symbol = "on"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 28)
    assert tenor.far_date == date(2023, 6, 29)
    ## t/n
    symbol = "t/n"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 29)
    assert tenor.far_date == date(2023, 6, 30)
    symbol = "tn"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 29)
    assert tenor.far_date == date(2023, 6, 30)
    ## s/n
    symbol = "s/n"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2023, 7, 3)
    symbol = "sn"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2023, 7, 3)
    symbol = "1wk"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2023, 7, 7)
    assert tenor.far.fixing == date(2023, 7, 6)
    assert tenor.far.mar == date(2023, 7, 5)
    ## 2wk
    symbol = "2wk"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2023, 7, 14)
    assert tenor.far.fixing == date(2023, 7, 13)
    assert tenor.far.mar == date(2023, 7, 12)
    ## 1m
    symbol = "1m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2023, 7, 31)
    assert tenor.far.fixing == date(2023, 7, 28)
    assert tenor.far.mar == date(2023, 7, 27)
    ## 2m
    symbol = "2m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2023, 8, 31)
    assert tenor.far.fixing == date(2023, 8, 30)
    assert tenor.far.mar == date(2023, 8, 29)
    ## 3m
    symbol = "3m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2023, 9, 27)
    assert tenor.far.fixing == date(2023, 9, 26)
    assert tenor.far.mar == date(2023, 9, 25)
    ## 4m
    symbol = "4m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2023, 10, 31)
    assert tenor.far.fixing == date(2023, 10, 30)
    assert tenor.far.mar == date(2023, 10, 27)
    ## 5m
    symbol = "5m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2023, 11, 30)
    assert tenor.far.fixing == date(2023, 11, 29)
    assert tenor.far.mar == date(2023, 11, 28)
    ## 6m
    symbol = "6m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2023, 12, 29)
    assert tenor.far.fixing == date(2023, 12, 28)
    assert tenor.far.mar == date(2023, 12, 27)
    ## 9m
    symbol = "9m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2024, 3, 29)
    assert tenor.far.fixing == date(2024, 3, 28)
    assert tenor.far.mar == date(2024, 3, 27)
    ## 12m
    symbol = "12m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2024, 6, 28)
    assert tenor.far.fixing == date(2024, 6, 27)
    assert tenor.far.mar == date(2024, 6, 26)

    # trade date 2023-06-29
    trade_date = date(2023, 6, 29)
    symbol = "spot"
    tenor = Tenor(symbol, trade_date)
    # spot
    assert tenor.spot == date(2023, 7, 3)
    ## o/n
    symbol = "o/n"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 29)
    assert tenor.far_date == date(2023, 6, 30)
    symbol = "on"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 29)
    assert tenor.far_date == date(2023, 6, 30)
    ## t/n
    symbol = "t/n"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2023, 7, 3)
    symbol = "tn"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 6, 30)
    assert tenor.far_date == date(2023, 7, 3)
    ## s/n
    symbol = "s/n"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 7, 3)
    assert tenor.far_date == date(2023, 7, 5)
    symbol = "sn"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 7, 3)
    assert tenor.far_date == date(2023, 7, 5)
    symbol = "1wk"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 7, 3)
    assert tenor.far_date == date(2023, 7, 10)
    assert tenor.far.fixing == date(2023, 7, 7)
    assert tenor.far.mar == date(2023, 7, 6)
    ## 2wk
    symbol = "2wk"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 7, 3)
    assert tenor.far_date == date(2023, 7, 17)
    assert tenor.far.fixing == date(2023, 7, 14)
    assert tenor.far.mar == date(2023, 7, 13)
    ## 1m
    symbol = "1m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 7, 3)
    assert tenor.far_date == date(2023, 8, 3)
    assert tenor.far.fixing == date(2023, 8, 2)
    assert tenor.far.mar == date(2023, 8, 1)
    ## 2m
    symbol = "2m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 7, 3)
    assert tenor.far_date == date(2023, 9, 5)
    assert tenor.far.fixing == date(2023, 9, 4)
    assert tenor.far.mar == date(2023, 9, 1)
    ## 3m
    symbol = "3m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 7, 3)
    assert tenor.far_date == date(2023, 10, 4)
    assert tenor.far.fixing == date(2023, 10, 2)
    assert tenor.far.mar == date(2023, 9, 27)
    ## 4m
    symbol = "4m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 7, 3)
    assert tenor.far_date == date(2023, 11, 3)
    assert tenor.far.fixing == date(2023, 11, 2)
    assert tenor.far.mar == date(2023, 11, 1)
    ## 5m
    symbol = "5m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 7, 3)
    assert tenor.far_date == date(2023, 12, 4)
    assert tenor.far.fixing == date(2023, 12, 1)
    assert tenor.far.mar == date(2023, 11, 30)
    ## 6m
    symbol = "6m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 7, 3)
    assert tenor.far_date == date(2024, 1, 3)
    assert tenor.far.fixing == date(2024, 1, 2)
    assert tenor.far.mar == date(2023, 12, 29)
    ## 9m
    symbol = "9m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 7, 3)
    assert tenor.far_date == date(2024, 4, 3)
    assert tenor.far.fixing == date(2024, 4, 2)
    assert tenor.far.mar == date(2024, 4, 1)
    ## 12m
    symbol = "12m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 7, 3)
    assert tenor.far_date == date(2024, 7, 3)
    assert tenor.far.fixing == date(2024, 7, 2)
    assert tenor.far.mar == date(2024, 7, 1)

    # trade date 2023-08-08
    trade_date = date(2023, 8, 8)
    symbol = "spot"
    tenor = Tenor(symbol, trade_date)
    # spot
    assert tenor.spot == date(2023, 8, 10)
    ## o/n
    symbol = "o/n"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 8)
    assert tenor.far_date == date(2023, 8, 9)
    symbol = "on"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 8)
    assert tenor.far_date == date(2023, 8, 9)
    ## t/n
    symbol = "t/n"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 9)
    assert tenor.far_date == date(2023, 8, 10)
    symbol = "tn"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 9)
    assert tenor.far_date == date(2023, 8, 10)
    ## s/n
    symbol = "s/n"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 10)
    assert tenor.far_date == date(2023, 8, 11)
    symbol = "sn"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 10)
    assert tenor.far_date == date(2023, 8, 11)
    symbol = "1wk"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 10)
    assert tenor.far_date == date(2023, 8, 17)
    assert tenor.far.fixing == date(2023, 8, 16)
    assert tenor.far.mar == date(2023, 8, 14)
    ## 2wk
    symbol = "2wk"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 10)
    assert tenor.far_date == date(2023, 8, 24)
    assert tenor.far.fixing == date(2023, 8, 23)
    assert tenor.far.mar == date(2023, 8, 22)
    ## 1m
    symbol = "1m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 10)
    assert tenor.far_date == date(2023, 9, 11)
    assert tenor.far.fixing == date(2023, 9, 8)
    assert tenor.far.mar == date(2023, 9, 7)
    ## 2m
    symbol = "2m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 10)
    assert tenor.far_date == date(2023, 10, 10)
    assert tenor.far.fixing == date(2023, 10, 6)
    assert tenor.far.mar == date(2023, 10, 5)
    ## 3m
    symbol = "3m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 10)
    assert tenor.far_date == date(2023, 11, 13)
    assert tenor.far.fixing == date(2023, 11, 10)
    assert tenor.far.mar == date(2023, 11, 9)
    ## 4m
    symbol = "4m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 10)
    assert tenor.far_date == date(2023, 12, 11)
    assert tenor.far.fixing == date(2023, 12, 8)
    assert tenor.far.mar == date(2023, 12, 7)
    ## 5m
    symbol = "5m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 10)
    assert tenor.far_date == date(2024, 1, 10)
    assert tenor.far.fixing == date(2024, 1, 9)
    assert tenor.far.mar == date(2024, 1, 8)
    ## 6m
    symbol = "6m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 10)
    assert tenor.far_date == date(2024, 2, 13)
    assert tenor.far.fixing == date(2024, 2, 8)
    assert tenor.far.mar == date(2024, 2, 7)
    ## 9m
    symbol = "9m"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 10)
    assert tenor.far_date == date(2024, 5, 10)
    assert tenor.far.fixing == date(2024, 5, 9)
    assert tenor.far.mar == date(2024, 5, 8)
    ## 12m
    symbol = "1y"
    tenor = Tenor(symbol, trade_date)
    assert tenor.near_date == date(2023, 8, 10)
    assert tenor.far_date == date(2024, 8, 12)
    assert tenor.far.fixing == date(2024, 8, 9)
    assert tenor.far.mar == date(2024, 8, 8)


def test_tenor_from_date():
    from_date = date(2024, 1, 1)
    to_date = from_date + relativedelta(years=2)
    tenor_symbols = [
        "spot",
        "on",
        "tn",
        "sn",
        "1w",
        "2w",
        "1m",
        "2m",
        "3m",
        "4m",
        "5m",
        "6m",
        "9m",
        "1y",
        "2y",
    ]
    tenor_symbols_length = len(tenor_symbols)
    total_start = time.time()
    tenors = []
    tenor_count = 0
    current_date = from_date
    while current_date <= to_date:
        current_date += timedelta(days=1)
        if not dateutils.is_working_day(current_date, "kr"):
            continue
        consume(tenors.append(Tenor(s, current_date)) for s in tenor_symbols)
        tenor_count += tenor_symbols_length
    duration = time.time() - total_start
    print(f"Took {round(duration, 2)}s to create {tenor_count} tenors")
    write_tenors_to_csv(tenors, "tenors.csv")


def write_tenors_to_csv(tenors: List[Tenor], filename: str):
    # Define the CSV headers
    headers = [
        "Tenor Symbol",
        "Trade Date",
        "Spot Date",
        "Leg1 Symbol",
        "Leg1 Value Date",
        "Leg1 Fixing Date",
        "Leg1 Mar Date",
        "Leg2 Symbol",
        "Leg2 Value Date",
        "Leg2 Fixing Date",
        "Leg2 Mar Date",
    ]

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for tenor in tenors:
            # Flatten the Tenor and Leg data
            row = [
                tenor.symbol,
                tenor.trade,
                tenor.spot,
                *flatten_leg(tenor.near),
                *flatten_leg(tenor.far),
            ]
            writer.writerow(row)


def flatten_leg(leg: Leg):
    # Extract the desired attributes from a Leg
    return [leg.symbol, leg.value, leg.fixing, leg.mar]
