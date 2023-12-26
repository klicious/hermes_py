# Function to parse YAML data and return a list of Bank instances
import os.path
from typing import Dict

import yaml

import constants
from .confirmation import Confirmation, Template

_TEMPLATES = {}
_CONFIRMATIONS = {}


def parse_yaml_to_confirmation(yaml_data) -> Dict[str, Confirmation]:
    return {
        key: Confirmation(
            entity=key,
            messenger=values.get("messenger", False),
            reuter=values.get("reuter", False),
            rtns=values.get("rtns", False),
            email=values.get("email", False),
            phone=values.get("phone", False),
            fax=values.get("fax", False),
        )
        for key, values in yaml_data.items()
    }


def parse_yaml_to_template(yaml_data) -> Dict[str, Template]:
    return {
        key: Template(
            entity=key,
            header=values.get("entity", ""),
            body=values.get("reuters", ""),
            tail=values.get("deposit-account", ""),
        )
        for key, values in yaml_data.items()
    }


def load_banks() -> None:
    file_path = os.path.join(constants.RESOURCE_DIR, "bank.yaml")
    with open(file_path, "r") as file:
        try:
            # Load the YAML content from file
            data = yaml.safe_load(file)
            _BANKS = parse_yaml_to_banks(data)
        except yaml.YAMLError as exc:
            print(f"Error in YAML file format: {exc}")


def get_banks() -> Dict[str, Bank]:
    return _BANKS


def get_bank(name: str) -> Bank | None:
    return _BANKS.get(name)


if not _BANKS:
    load_banks()
