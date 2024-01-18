"""This script is an API client for hunter.io.

https://hunter.io/api-documentation/v2

It provides next functionality:
- look for email addresses for provided domain name;
- look for emails by the owner first and last mane;
- get info about email address accessibility.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, List

from hunter_client.hunter_api_client import HunterClient
from hunter_client.hunter_client_types import EmailAccessData, EmailBaseData
from hunter_client.parsers import (
    parse_email_by_domain_first_last_name_data,
    parse_emails_by_domain_data,
    parse_verify_email_data,
)

endpoint_data = dict[str, EmailBaseData] | dict[str, EmailAccessData]


class AbstractEndpoint(ABC):
    """Class represents endpoint abstraction. Contain common endpoints logic."""

    path: str

    def __init__(self, api_key: str) -> None:
        """Init AbstractEndpoint with hunter.io API key and hunter_client."""
        self.api_key = api_key
        self.hunter_client = HunterClient()

    @abstractmethod
    def execute(self, *args: Any) -> endpoint_data:
        """Abstract execute method."""

    def execute_request(
        self, method: str, path: str, url_params: dict, parser: Callable[[dict], endpoint_data],
    ) -> endpoint_data:
        """Execute request via API client and parse response."""
        response = self.hunter_client.send_request(method, path, url_params)
        return parser(response)


class EndpointFactory(object):
    """Factory class for endpoints."""

    def __init__(self, api_key: str) -> None:
        """Init EndpointFactory with hunter.io API key."""
        self.api_key = api_key

    def get_endpoint(self, path: str) -> AbstractEndpoint:
        """Get endpoint according to provided path."""
        endpoints: List = list(AbstractEndpoint.__subclasses__())
        for endpoint in endpoints:
            if endpoint.path == path:
                return endpoint(self.api_key)
        raise NotImplementedError('Endpoint not implemented')


class EmailsByDomain(AbstractEndpoint):
    """Endpoint for getting emails by domain."""

    path = 'domain-search'

    def __init__(self, api_key: str) -> None:
        """Init EmailsByDomain class with path and parser."""
        self.parser = parse_emails_by_domain_data
        super().__init__(api_key)

    def execute(self, method: str, domain: str) -> endpoint_data:
        """Look for emails by specified domain."""
        params_for_url = {'domain': domain, 'api_key': self.api_key}
        return self.execute_request(method, self.path, params_for_url, self.parser)


class EmailByDomainFirstLastName(AbstractEndpoint):
    """Endpoint for getting emails by domain,  first, last names."""

    path = 'email-finder'

    def __init__(self, api_key: str) -> None:
        """Init EmailByDomainFirstLastName class with path and parser."""
        self.parser = parse_email_by_domain_first_last_name_data
        super().__init__(api_key)

    def execute(self, method: str, domain: str, first_name: str, last_name: str) -> endpoint_data:
        """Look for email by specified domain, first name, last name."""
        params_for_url = {'domain': domain, 'first_name': first_name, 'last_name': last_name, 'api_key': self.api_key}
        return self.execute_request(method, self.path, params_for_url, self.parser)


class EmailVerification(AbstractEndpoint):
    """Endpoint for verifying email."""

    path = 'email-verifier'

    def __init__(self, api_key: str) -> None:
        """Init EmailVerification class with path and parser."""
        self.parser = parse_verify_email_data
        super().__init__(api_key)

    def execute(self, method: str, email: str) -> endpoint_data:
        """Verify specified email address accessibility."""
        params_for_url = {'email': email, 'api_key': self.api_key}
        return self.execute_request(method, self.path, params_for_url, self.parser)
