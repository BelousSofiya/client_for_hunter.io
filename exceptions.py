"""Hunter Client exceptions."""


class HunterClientHTTPError(Exception):
    """Raise when API response status is not 200."""

    def __init__(self, status: int, message: str):
        """Init HunterClientHTTPError with status and error message."""
        self.status = status
        self.message = message


class HunterClientDataError(Exception):
    """Rise when API response contains unexpected data."""

    def __init__(self, message: str):
        """Init HunterClientDataError with error message."""
        self.message = message
