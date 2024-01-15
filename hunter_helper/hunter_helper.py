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

    def get_emails_by_domain(self, domain: str) -> expected_dict:
        """Look for emails by specified domain."""
        params_for_url = {'domain': domain, 'api_key': self.api_key}
        return self.execute_request_template('domain-search', params_for_url, parse_emails_by_domain_data)

    def get_email_by_domain_first_last_name(
        self, domain: str, first_name: str, last_name: str,
    ) -> expected_dict:
        """Look for email by specified domain, first name, last name."""
        params_for_url = {'domain': domain, 'first_name': first_name, 'last_name': last_name, 'api_key': self.api_key}
        return self.execute_request_template('email-finder', params_for_url, parse_email_by_domain_first_last_name_data)

    def verify_email(self, email: str) -> dict[str, ParserDict] | dict[str, UpdateDict]:
        """Verify specified email address accessibility."""
        params_for_url = {'email': email, 'api_key': self.api_key}
        return self.execute_request_template('email-verifier', params_for_url, parse_verify_email_data)
