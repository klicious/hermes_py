# Function to parse YAML data and return a list of Bank instances
import os.path
from typing import Dict, Set

import yaml

import constants
from .bank import Bank

_BANKS = {}


def parse_yaml_to_banks(yaml_data) -> Dict[str, Bank]:
    return {
        key: Bank(
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


def load_banks() -> None:
    file_path = os.path.join(constants.RESOURCE_DIR, "bank.yaml")
    with open(file_path, "r") as file:
        try:
            # Load the YAML content from file
            data = yaml.safe_load(file)
            _BANKS.update(parse_yaml_to_banks(data))
        except yaml.YAMLError as exc:
            print(f"Error in YAML file format: {exc}")


def get_banks() -> Dict[str, Bank]:
    return _BANKS


def get_bank(name: str) -> Bank | None:
    return _BANKS.get(name)


def get_bank_names() -> Set[str]:
    return set(get_banks().keys())


if not _BANKS:
    load_banks()
