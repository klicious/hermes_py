from typing import List

from application import confirmation as cfm
from application.confirmation import Confirmation, Type as CfmType
from .trade_fixtures import TRADES


def test_confirmation_cx():
    confirmation_type = CfmType.REUTER
    confirmations: List[Confirmation] = cfm.confirm(TRADES, confirmation_type)
    print(f"{len(confirmations)} confirmations")
    cfm_cx_msgs = [msg for c in confirmations for msg in c.cx().values()]
    print("======================== MSG ========================\n".join(cfm_cx_msgs))
