# Function to parse YAML data and return a list of Bank instances
import os.path
from typing import Dict, Set

import yaml

import constants
from .house import House

_HOUSES = {}


def parse_yaml_to_banks(yaml_data) -> Dict[str, House]:
    return {
        key: House(
            name=key,
            full_name=values.get("full-name", ""),
            entity=values.get("entity", ""),
            reuters=values.get("reuters", ""),
            deposit_account=values.get("deposit-account", ""),
            bro=values.get("bro", 0),
            bro_currency=values.get("bro-currency", ""),
            remark=values.get("remark", ""),
            quad_code=values.get("quad-code", ""),
        )
        for key, values in yaml_data.items()
    }


def load_houses() -> None:
    file_path = os.path.join(constants.RESOURCE_DIR, "house.yaml")
    with open(file_path, "r") as file:
        try:
            # Load the YAML content from file
            data = yaml.safe_load(file)
            _HOUSES.update(parse_yaml_to_banks(data))
        except yaml.YAMLError as exc:
            print(f"Error in YAML file format: {exc}")


def get_houses() -> Dict[str, House]:
    return _HOUSES


def get_house(name: str) -> House | None:
    return _HOUSES.get(name)


def get_house_names() -> Set[str]:
    return set(get_houses().keys())


if not _HOUSES:
    load_houses()
