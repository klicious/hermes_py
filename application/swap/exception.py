class InvalidTenorDateException(Exception):
    """Exception raised for errors in the input date.

    Attributes:
        date -- input date which caused the error
        message -- explanation of the error
    """

    def __init__(self, date, message="Invalid tenor date provided"):
        self.date = date
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.date} -> {self.message}"
