import uuid

from adapter.google import sheets

_EXPANSION_TO_ABBREVIATION = {}
_ABBREVIATION_TO_EXPANSION = {}
_NICKNAME_TO_TRADER = {}


def init():
    __load_abbreviations()
    __load_nicknames()


def __load_abbreviations():
    values = sheets.get_values("abbreviations", "A:B")
    expansion_to_abbreviation = {o.get("expansion", ""): o for o in values}
    abbreviation_to_expansion = {o.get("abbreviation", ""): o for o in values}
    _EXPANSION_TO_ABBREVIATION.update(expansion_to_abbreviation)
    _ABBREVIATION_TO_EXPANSION.update(abbreviation_to_expansion)


def __load_nicknames():
    values = sheets.get_values("nicknames", "A:D")
    nickname_to_trader = {o.get("nickname", ""): __to_trader(o) for o in values}
    _NICKNAME_TO_TRADER.update(nickname_to_trader)


def __to_trader(o) -> dict:
    return {
        "symbol": f"{o.get('house')} {get_abbreviation(o.get('entity', ''))}",
        "house": o.get("house", ""),
        "entity": o.get("entity", ""),
        "trader": o.get("trader", ""),
    }


def generate_uuid() -> str:
    return str(uuid.uuid4())


def get_trader(nickname: str):
    if not _NICKNAME_TO_TRADER:
        init()
    return _NICKNAME_TO_TRADER.get(
        nickname, {"symbol": "", "house": "", "entity": "", "trader": ""}
    )


def get_expansion(abbreviation: str):
    if not _ABBREVIATION_TO_EXPANSION:
        init()
    return _ABBREVIATION_TO_EXPANSION.get(abbreviation, abbreviation)


def get_abbreviation(expansion: str):
    if not _EXPANSION_TO_ABBREVIATION:
        init()
    return _EXPANSION_TO_ABBREVIATION.get(expansion, expansion)
