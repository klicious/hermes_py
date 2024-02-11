from dataclasses import dataclass

from . import utils


@dataclass
class House:
    name: str
    full_name: str
    entity: str
    reuters: str
    deposit_account: str
    bro: int
    bro_currency: str
    remark: str
    quad_code: str

    @property
    def house_abbreviation(self):
        return utils.entity_abbreviation(self.entity)

    def house_with_entity(self):
        return f"{self.name} {self.house_abbreviation}"
