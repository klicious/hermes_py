from dataclasses import dataclass, field

from . import utils


@dataclass
class House:
    name: str
    full_name: str
    entity: str
    reuter_code: str = field(default="")
    deposit_account: str = field(default="")
    quad_code: str = field(default="")
    remark: str = field(default="")

    def __post_init__(self) -> None:
        self.name = self.name.upper()
        self.full_name = self.full_name.upper()
        self.entity = self.entity.upper()
        self.reuter_code = self.reuter_code.upper()
        self.deposit_account = self.deposit_account.upper()
        self.quad_code = self.quad_code.upper()

    @property
    def entity_abbreviation(self):
        return utils.entity_abbreviation(self.entity)

    def house_with_entity(self):
        return f"{self.name} {self.entity_abbreviation}"
