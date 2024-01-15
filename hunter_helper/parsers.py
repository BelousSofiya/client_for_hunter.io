"""Parsers for hunter_helper.py."""

from typing import Dict
from uuid import uuid4

from data_storage_types import UpdateDict
from hunter_helper.exceptions import HunterClientDataError
from hunter_helper.hunter_client_types import ParserDict


def parse_emails_by_domain_data(response: dict) -> Dict[str, ParserDict]:
    """Parser for get emails by domain method."""
    try:
        return _parse_emails_by_domain_data(response)
    except KeyError:
        raise HunterClientDataError('Failed to parse hunter.io response')


def _parse_emails_by_domain_data(response: dict) -> Dict[str, ParserDict]:
    new_emails_dict: Dict[str, ParserDict] = {}

    for email in response['data']['emails']:
        domains = []

        for source in email['sources']:
            domains.append(source['domain'])

        email_id = str(uuid4())
        new_emails_dict.update({email['value']: {'id': email_id, 'domains': domains}})
    return new_emails_dict


def parse_email_by_domain_first_last_name_data(response: dict) -> Dict[str, ParserDict]:
    """Parser for get email by domain, first, last name method."""
    try:
        return _parse_email_by_domain_first_last_name_data(response)
    except KeyError:
        raise HunterClientDataError('Failed to parse hunter.io response')


def _parse_email_by_domain_first_last_name_data(response: dict) -> Dict[str, ParserDict]:
    domains = []
    for source in response['data']['sources']:
        domains.append(source['domain'])
    email_id = str(uuid4())
    return {response['data']['email']: {'id': email_id, 'domains': domains}}


def parse_verify_email_data(response: dict) -> dict[str, UpdateDict]:
    """Parser for verify email method."""
    try:
        return _parse_verify_email_data(response)
    except KeyError:
        raise HunterClientDataError('Failed to parse hunter.io response')


def _parse_verify_email_data(response: dict) -> Dict[str, UpdateDict]:
    email = response['data']['email']
    status_from_response = response['data']['status']
    result_from_response = response['data']['result']
    return {email: {'email_status': status_from_response, 'email_result': result_from_response}}
