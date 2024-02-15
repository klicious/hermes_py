from application.swap.fee import fee


def test_calculate_fee():
    df_fee = fee.calculate_fee("woori sl", "df", "1m", 1)
    print(df_fee)
