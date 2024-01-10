"""Class to store emails data."""

from hunter_client_types import UpdateDict


class ClientDataStore(object):
    """Data storage."""

    def __init__(self) -> None:
        """Init ClientDataStore class with own_data."""
        self.own_data: dict = {}

    def add_emails(self, emails_dict: dict) -> None:
        """Add emails to data storage."""
        for email in emails_dict.keys():
            if email not in self.own_data:
                self.own_data[email] = emails_dict[email]

    def update_email(self, email: str, new_data: UpdateDict) -> None:
        """Update email in data storage."""
        if email in self.own_data.keys():
            self.own_data[email].update(new_data)
