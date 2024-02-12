# Function to parse YAML data and return a list of Bank instances
import os.path
from typing import Dict, Set

import yaml

import constants
from utils import fileutils
from .house import House

_NAME_TO_HOUSE = {}


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


def load_houses_yaml() -> None:
    file_path = os.path.join(constants.RESOURCE_DIR, "house", "house.yaml")
    with open(file_path, "r") as file:
        try:
            data = yaml.safe_load(file)
            _NAME_TO_HOUSE.update(parse_yaml_to_banks(data))
        except yaml.YAMLError as exc:
            print(f"Error in YAML file format: {exc}")


def load_houses_csv() -> None:
    file_path = os.path.join(constants.RESOURCE_DIR, "house", "house.csv")
    name_to_house = {
        h.get("name", ""): House(**h) for h in fileutils.read_csv_to_dicts(file_path)
    }
    _NAME_TO_HOUSE.update(name_to_house)


def get_name_to_house() -> Dict[str, House]:
    return _NAME_TO_HOUSE


def get_house(name: str) -> House | None:
    return _NAME_TO_HOUSE.get(name)


def get_house_names() -> Set[str]:
    return set(get_name_to_house().keys())


if not _NAME_TO_HOUSE:
    load_houses_csv()
