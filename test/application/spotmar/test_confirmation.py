import itertools
from typing import List

import application.spotmar.confirmation as cfm
from application.confirmation import Confirmation, Type as CfmType
from .trade_fixtures import TRADES


def test_reuter():
    messages = cfm.reuter(TRADES)

    print(
        "\n".join(
            m.full
            for m in itertools.chain.from_iterable(msgs for msgs in messages.values())
        )
    )
    print(f"{sum(len(m) for m in messages.values())} messages")


def test_confirmation_cx():
    confirmation_type = CfmType.REUTER
    confirmations: List[Confirmation] = cfm.confirm(TRADES, confirmation_type)
    print(f"{len(confirmations)} confirmations")
    cfm_cx_msgs = [c.rx() for c in confirmations]
    print("======================== MSG ========================\n".join(cfm_cx_msgs))
