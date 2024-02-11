_ENTITY = {
    "sl": "seoul",
    "hk": "hong kong",
    "ldn": "london",
    "nyk": "new york",
}
_ENTITY_ABBREVIATION = {
    "seoul": "sl",
    "hong kong": "hk",
    "london": "ldn",
    "new york": "nyk",
}


def entity(abbreviation: str) -> str:
    return _ENTITY.get(abbreviation, abbreviation)


def entity_abbreviation(name: str) -> str:
    return _ENTITY_ABBREVIATION.get(name, name)
