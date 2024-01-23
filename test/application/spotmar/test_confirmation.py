import application.spotmar.confirmation as cfm
from .trade_fixtures import TRADES


def test_reuter():
    messages = cfm.reuter(TRADES)
    print(messages)
