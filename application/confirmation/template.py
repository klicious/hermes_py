from dataclasses import dataclass


class Confirmation:
    entity: str
    messenger: bool
    reuter: bool
    rtns: bool
    email: bool
    phone: bool
    fax: bool


@dataclass
class Template:
    entity: str
    header: str
    body: str
    tail: str
