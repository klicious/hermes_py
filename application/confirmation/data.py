import os.path
from typing import Dict, Any

import yaml

import constants
from .method import Method
from .template import Template
from .type import Type as ConfirmationType

_REUTER_TEMPLATES = {}
_CONFIRMATION_METHODS = {}

_TEMPLATES = {ConfirmationType.REUTER: _REUTER_TEMPLATES}

SPOT_MAR = "spotmar"
SWAP = "swap"
_products = [SPOT_MAR, SWAP]


def __parse_yaml_to_confirmation_method(yaml_data, product) -> Dict[str, Method]:
    return {
        key: Method.of(
            entity=key,
            product=product,
            messenger=values.get("messenger", False),
            reuter=values.get("reuter", False),
            rtns=values.get("rtns", False),
            email=values.get("email", False),
            phone=values.get("phone", False),
            fax=values.get("fax", False),
        )
        for key, values in yaml_data.items()
    }


def __parse_yaml_to_template(yaml_data, _type: ConfirmationType) -> Dict[str, Template]:
    return {
        key: Template(
            entity=key,
            type=_type,
            header=values.get("header", ""),
            body=values.get("body", ""),
            tail=values.get("tail", ""),
        )
        for key, values in yaml_data.items()
    }


def __load_confirmation_methods() -> None:
    for product in _products:
        file_path = os.path.join(
            constants.RESOURCE_DIR, "confirmation", product, "list.yaml"
        )
        with open(file_path, "r") as file:
            try:
                # Load the YAML content from file
                data = yaml.safe_load(file)
                _CONFIRMATION_METHODS[product] = __parse_yaml_to_confirmation_method(
                    data, product
                )
            except yaml.YAMLError as exc:
                print(f"Error in YAML file format: {exc}")


def __load_reuter_templates() -> None:
    confirmation_type = ConfirmationType.REUTER
    for product in _products:
        file_path = os.path.join(
            constants.RESOURCE_DIR,
            "confirmation",
            product,
            f"{confirmation_type.value}.yaml",
        )
        with open(file_path, "r") as file:
            try:
                # Load the YAML content from file
                data = yaml.safe_load(file)
                _REUTER_TEMPLATES[product] = __parse_yaml_to_template(
                    data, ConfirmationType.REUTER
                )
            except yaml.YAMLError as exc:
                print(f"Error in YAML file format: {exc}")


def get_confirmation_method(product: str, entity: str) -> Method | None:
    initialize_data()
    cfm_methods = _CONFIRMATION_METHODS[product]
    return _get(cfm_methods, entity)


def get_template(
    product: str, entity: str, cfm_type: ConfirmationType
) -> Template | None:
    templates = _TEMPLATES.get(cfm_type, {}).get(product, {})
    if templates:
        return _get(templates, entity)


def get_reuter_template(product: str, entity: str) -> Template | None:
    initialize_data()
    templates = _REUTER_TEMPLATES[product]
    return _get(templates, entity)


def _get(d: Dict[str, Any], entity: str) -> Any | None:
    if entity in d and not d[entity].is_empty():
        return d[entity]
    return d.get("default", None)


def initialize_data():
    if not _REUTER_TEMPLATES:
        __load_reuter_templates()
        __load_confirmation_methods()


initialize_data()
