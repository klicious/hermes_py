import os.path
from typing import Dict, Any

import yaml
from more_itertools import consume

import constants
from adapter.google import sheets
from .method import Method
from .template import Template
from .type import Type as ConfirmationType, Type

_REUTER_TEMPLATES = {}
_CONFIRMATION_METHODS = {}

_TEMPLATES = {ConfirmationType.REUTER: _REUTER_TEMPLATES}

SPOT_MAR = "spotmar"
SWAP_DF = "df"
SWAP_NDF = "nd"
_products = [SPOT_MAR, SWAP_DF, SWAP_NDF]


def __parse_yaml_to_confirmation_method(yaml_data, product) -> Dict[str, Method]:
    return {
        key: Method.of(
            house=key,
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
            house=key,
            type=_type,
            header=values.get("header", ""),
            body=values.get("body", ""),
            tail=values.get("tail", ""),
        )
        for key, values in yaml_data.items()
    }


def __load_confirmation_methods_from_file() -> None:
    for product in _products:
        product_path = os.path.join(*product.split("-"))
        file_path = os.path.join(
            constants.RESOURCE_DIR, "confirmation", *product_path, "list.yaml"
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


def __load_reuter_templates_from_file() -> None:
    confirmation_type = ConfirmationType.REUTER
    for product in _products:
        product_path = os.path.join(*product.split("-"))
        file_path = os.path.join(
            constants.RESOURCE_DIR,
            "confirmation",
            *product_path,
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


def __load_confirmation_methods():
    consume(__load_confirmation_methods_from_google_sheet(p) for p in _products)


def __load_confirmation_methods_from_google_sheet(product: str):
    cfm_methods = [
        Method.of(
            house=cm.get("house").strip().upper(),
            product=product,
            messenger=True if cm.get("Messenger", "").strip().upper() == "O" else False,
            rtns=True if cm.get("RTNS", "").strip().upper() == "O" else False,
            reuter=True if cm.get("Reuter", "").strip().upper() == "O" else False,
            email=True if cm.get("E-mail", "").strip().upper() == "O" else False,
            phone=True if cm.get("Phone", "").strip().upper() == "O" else False,
            fax=True if cm.get("Fax", "").strip().upper() == "O" else False,
        )
        for cm in sheets.get_values(f"{product} confirmation methods", "A:G")
    ]
    _CONFIRMATION_METHODS[product.upper()] = {m.house: m for m in cfm_methods}


def __load_templates():
    consume(__load_templates_from_google_sheet(p) for p in _products)


def __load_templates_from_google_sheet(product: str):
    _type = Type.REUTER
    _REUTER_TEMPLATES[product.upper()] = {
        t.get("house", "")
        .upper()
        .strip(): Template(
            house=t.get("house", "").upper().strip(),
            type=_type,
            header=t.get("header", "").lower().strip(),
            body=t.get("body", "").lower().strip(),
            tail=t.get("tail", "").lower().strip(),
        )
        for t in sheets.get_values(f"{product} confirmation message templates", "C:F")
        if t.get("house")
    }


def get_confirmation_method(product: str, house: str) -> Method | None:
    if not _CONFIRMATION_METHODS:
        init()
    cfm_methods = _CONFIRMATION_METHODS[product.upper()]
    return _get(cfm_methods, house)


def get_template(
    product: str, house: str, cfm_type: ConfirmationType = ConfirmationType.REUTER
) -> Template | None:
    if not _REUTER_TEMPLATES:
        init()
    templates = _TEMPLATES.get(cfm_type, {}).get(product.upper(), {})
    if templates:
        return _get(templates, house.upper())


def _get(d: Dict[str, Any], entity: str) -> Any | None:
    if entity in d and not d[entity].is_empty():
        return d[entity]
    return d.get("DEFAULT", None)


def init():
    __load_templates()
    __load_confirmation_methods()


if not _REUTER_TEMPLATES:
    init()
