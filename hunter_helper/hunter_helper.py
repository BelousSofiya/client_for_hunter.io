"""This script is an API client for hunter.io.

https://hunter.io/api-documentation/v2

It provides next functionality:
- look for email addresses for provided domain name;
- look for emails by the owner first and last mane;
- get info about email address accessibility;
- get collected data about observed emails.
"""

from typing import Callable

from data_storage_types import UpdateDict
from hunter_helper.hunter_api_client import HunterClient
from hunter_helper.hunter_client_types import ParserDict
from hunter_helper.parsers import (
    parse_email_by_domain_first_last_name_data,
    parse_emails_by_domain_data,
    parse_verify_email_data,
)

expected_dict = dict[str, ParserDict] | dict[str, UpdateDict]


class HunterHelper(object):
    """Main class containing API methods."""

    def __init__(self, api_key: str) -> None:
        """Init HunterHelper with hunter.io API key and support classes."""
        self.api_key = api_key
        self.hunter_client = HunterClient()

    def execute_request_template(
        self, path: str, url_params: dict, parser: Callable[[dict], expected_dict],
    ) -> expected_dict:
        """Execute request via API client and parse response."""
        response = self.hunter_client.get(path, url_params)
        return parser(response)


class EmailsByDomain(HunterHelper):
    """Endpoint for getting emails by domain."""

    def __init__(self, api_key: str) -> None:
        """Init EmailsByDomain class with path and parser."""
        self.path = 'domain-search'
        self.parser = parse_emails_by_domain_data
        super().__init__(api_key)

    def execute(self, domain: str) -> expected_dict:
        """Look for emails by specified domain."""
        params_for_url = {'domain': domain, 'api_key': self.api_key}
        return self.execute_request_template(self.path, params_for_url, self.parser)


class EmailByDomainFirstLastName(HunterHelper):
    """Endpoint for getting emails by domain, first, last names."""

    def __init__(self, api_key: str) -> None:
        """Init EmailByDomainFirstLastName class with path and parser."""
        self.path = 'email-finder'
        self.parser = parse_email_by_domain_first_last_name_data
        super().__init__(api_key)

    def execute(self, domain: str, first_name: str, last_name: str) -> expected_dict:
        """Look for email by specified domain, first name, last name."""
        params_for_url = {'domain': domain, 'first_name': first_name, 'last_name': last_name, 'api_key': self.api_key}
        return self.execute_request_template(self.path, params_for_url, self.parser)


class EmailVerification(HunterHelper):
    """Endpoint for verifying email."""

    def __init__(self, api_key: str) -> None:
        """Init EmailVerification class with path and parser."""
        self.path = 'email-verifier'
        self.parser = parse_verify_email_data
        super().__init__(api_key)

    def execute(self, email: str) -> dict[str, ParserDict] | dict[str, UpdateDict]:
        """Verify specified email address accessibility."""
        params_for_url = {'email': email, 'api_key': self.api_key}
        return self.execute_request_template(self.path, params_for_url, self.parser)
