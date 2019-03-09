class Error(Exception):
    """
    Base class for other exceptions

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class UnsupportedChartError(Error):
    """
    Exception raised for unsupported graph error.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message


class ColumnNameError(Error):
    """
    Exception raised for column name error.

    Attributes:
        message -- explanation of the error
    """
    def __init__(self, message):
        self.message = message
