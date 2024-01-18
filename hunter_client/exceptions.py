"""Hunter Client exceptions."""


class HunterClientDataError(Exception):
    """Rise when API response contains unexpected data."""

    def __init__(self, message: str):
        """Init HunterClientDataError with error message."""
        self.message = message
