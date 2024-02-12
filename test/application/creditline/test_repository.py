from application.creditline import repository


def test_get_credit_line():
    credit_line = repository.get_credit_line("anz", "bbva", "swap", "spot")
    print(credit_line)
