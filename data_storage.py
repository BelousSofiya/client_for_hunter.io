"""Class to store emails data."""

from data_storage_types import UpdateDict
from hunter_helper.hunter_client_types import ParserDict

expected_dict = dict[str, ParserDict] | dict[str, UpdateDict]


class ClientDataStore(object):
    """Data storage."""

    def __init__(self) -> None:
        """Init ClientDataStore class with own_data."""
        self.own_data: dict = {}

    def add_emails(self, emails_dict: expected_dict) -> None:
        """Add emails to data storage."""
        for email in emails_dict.keys():
            if email not in self.own_data:
                self.own_data[email] = emails_dict[email]

    def update_email(self, email: str, new_data: expected_dict) -> None:
        """Update email in data storage."""
        if email in self.own_data.keys():
            self.own_data[email].update(new_data)
