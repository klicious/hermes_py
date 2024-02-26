from application import spotmar


def test_fee():
    fee = spotmar.get_fee("anz sl")
    print(fee)
