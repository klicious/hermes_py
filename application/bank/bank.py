from dataclasses import dataclass


@dataclass
class Bank:
    name: str
    full_name: str
    entity: str
    reuters: str
    deposit_account: str
    bro: int
    bro_currency: str
    remark: str
    quad_code: str
