import itertools

import application.spotmar.confirmation as cfm
from .trade_fixtures import TRADES


def test_reuter():
    messages = cfm.reuter(TRADES)

    print("\n".join(m.full for m in itertools.chain.from_iterable(msgs for msgs in messages.values())))
    print(f"{sum(len(m) for m in messages.values())} messages")
