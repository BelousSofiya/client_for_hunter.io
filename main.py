"""This script is an API client for hunter.io.

https://hunter.io/api-documentation/v2

It provides next functionality:
- look for email addresses for provided domain name;
- look for emails by the owner first and last mane;
- get info about email address accessibility;
- get collected data about observed emails.
"""

from typing import Dict

from api_client import HunterClient
from data_storage import ClientDataStore
from hunter_client_types import MainDataDict, UpdateDict
from parsers import parse_email_by_domain_first_last_name_data, parse_emails_by_domain_data, parse_verify_email_data


class HunterHelper(object):
    """Main class containing API methods."""

    def __init__(self, api_key: str) -> None:
        """Init HunterHelper with hunter.io API key and support classes."""
        self.api_key = api_key
        self.hunter_client = HunterClient()
        self.data_store = ClientDataStore()

    def get_emails_by_domain(self, domain: str) -> list[str]:
        """Look for emails by specified domain."""
        params_for_url = {'domain': domain, 'api_key': self.api_key}
        response = self.hunter_client.get('domain-search', params_for_url)
        emails_dict = parse_emails_by_domain_data(response)
        self.data_store.add_emails(emails_dict)
        emails_list = []
        for email in emails_dict:
            emails_list.append(email)
        return emails_list

    def get_email_by_domain_first_last_name(self, domain: str, first_name: str, last_name: str) -> str:
        """Look for email by specified domain, first name, last name."""
        params_for_url = {'domain': domain, 'first_name': first_name, 'last_name': last_name, 'api_key': self.api_key}
        response = self.hunter_client.get('email-finder', params_for_url)
        email_dict = parse_email_by_domain_first_last_name_data(response)
        self.data_store.add_emails(email_dict)
        return list(email_dict.keys())[0]

    def verify_email(self, email: str) -> UpdateDict:
        """Verify specified email address accessibility."""
        params_for_url = {'email': email, 'api_key': self.api_key}
        response = self.hunter_client.get('email-verifier', params_for_url)
        dict_for_update_email = parse_verify_email_data(response)
        self.data_store.update_email(email, dict_for_update_email)
        return dict_for_update_email

    def get_all_data(self) -> Dict[str, MainDataDict]:
        """Get all stored emails data."""
        return self.data_store.own_data


if __name__ == '__main__':
    client = HunterHelper('e93c41dd45281f55bbb854ec1e86719c50b90d5d')
    email_by_domain_first_last_name = client.get_email_by_domain_first_last_name('reddit.com', 'Alexis', 'Ohanian')
    emails_by_domain = client.get_emails_by_domain('stripe.com')
    email_verified = client.verify_email('patrik@stripe.com')
