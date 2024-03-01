# Function to parse YAML data and return a list of Bank instances
import os.path
from typing import Dict, Set

import yaml

import constants
from adapter.google import sheets
from utils import fileutils
from .house import House

_SYMBOL_TO_HOUSE = {}


def parse_yaml_to_banks(yaml_data) -> Dict[str, House]:
    return {
        key: House(
            name=key,
            full_name=values.get("full-name", ""),
            entity=values.get("entity", ""),
            reuter_code=values.get("reuters", ""),
            deposit_account=values.get("deposit-account", ""),
            remark=values.get("remark", ""),
            quad_code=values.get("quad-code", ""),
        )
        for key, values in yaml_data.items()
    }


def _load_houses_yaml() -> None:
    file_path = os.path.join(constants.RESOURCE_DIR, "house", "house.yaml")
    with open(file_path, "r") as file:
        try:
            data = yaml.safe_load(file)
            _SYMBOL_TO_HOUSE.update(parse_yaml_to_banks(data))
        except yaml.YAMLError as exc:
            print(f"Error in YAML file format: {exc}")


def _load_houses_csv() -> None:
    file_path = os.path.join(constants.RESOURCE_DIR, "house", "house.csv")
    name_to_house = {
        h.get("name", ""): House(**h) for h in fileutils.read_csv_to_dicts(file_path)
    }
    _SYMBOL_TO_HOUSE.update(name_to_house)


def _load_houses_google_sheets() -> None:
    name_to_house = {
        h.get("name", ""): House(**h) for h in sheets.get_values("houses", "A:F")
    }
    _SYMBOL_TO_HOUSE.update(name_to_house)


def get_name_to_house() -> Dict[str, House]:
    return _SYMBOL_TO_HOUSE


def get_house(symbol: str) -> House | None:
    return _SYMBOL_TO_HOUSE.get(symbol)


def get_house_names() -> Set[str]:
    return set(get_name_to_house().keys())


if not _SYMBOL_TO_HOUSE:
    _load_houses_google_sheets()
