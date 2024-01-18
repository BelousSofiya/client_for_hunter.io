from unittest import TestCase
from unittest.mock import patch

from hunter_client.exceptions import HunterClientDataError
from hunter_client.parsers import (
    parse_emails_by_domain_data,
    parse_email_by_domain_first_last_name_data,
    parse_verify_email_data,
)


class ParseEmailsByDomainDataTests(TestCase):

    @patch("hunter_client.parsers.uuid4")
    def test_success(self, mock_uuid):
        test_data = {
            'data': {
                'emails': [
                    {
                        'value': 'test_email_1',
                        'sources': [
                            {'domain': 'test_domain_1'},
                            {'domain': 'test_domain_2'},
                        ]
                    },
                    {
                        'value': 'test_email_2',
                        'sources': [{'domain': 'test_domain_3'}, ]
                    }
                ]
            }
        }
        mock_uuid.side_effect = ['17465ddf-ef37-4b62-a142-ef9b37c032b8', 'd5f76e62-4add-40ec-9a1c-ce8e89290f88']

        actual = parse_emails_by_domain_data(test_data)
        expected = {'test_email_1': {'domains': ['test_domain_1', 'test_domain_2'],
                                     'id': '17465ddf-ef37-4b62-a142-ef9b37c032b8'},
                    'test_email_2': {'domains': ['test_domain_3'],
                                     'id': 'd5f76e62-4add-40ec-9a1c-ce8e89290f88'}}

        self.assertEqual(expected, actual)

    def test_parse_failing_rises_exception(self):
        test_data = {"incorrect": "data"}

        with self.assertRaises(HunterClientDataError):
            parse_emails_by_domain_data(test_data)


class ParseEmailByDomainFirstLastNameDataTests(TestCase):

    @patch("hunter_client.parsers.uuid4")
    def test_success(self, mock_uuid):
        test_data = {'data':  {
            'email': 'test_email_1',
            'sources': [
                    {'domain': 'test_domain_1'},
                    {'domain': 'test_domain_2'},
                ]
                }}
        mock_uuid.side_effect = ['17465ddf-ef37-4b62-a142-ef9b37c032b8']

        actual = parse_email_by_domain_first_last_name_data(test_data)
        expected = {'test_email_1': {'domains': ['test_domain_1', 'test_domain_2'],
                                     'id': '17465ddf-ef37-4b62-a142-ef9b37c032b8'}}

        self.assertEqual(expected, actual)

    def test_parse_failing_rises_exception(self):
        test_data = {"incorrect": "data"}

        with self.assertRaises(HunterClientDataError):
            parse_email_by_domain_first_last_name_data(test_data)


class ParseVerifyEmailDataTests(TestCase):

    def test_success(self):
        test_data = {"data": {
            "email": "test_email_1",
            "status": "accept_all",
            "result": "risky"}}

        actual = parse_verify_email_data(test_data)
        expected = {'test_email_1': {'email_status': 'accept_all', 'email_result': 'risky'}}

        self.assertEqual(expected, actual)

    def test_parse_failing_rises_exception(self):
        test_data = {"incorrect": "data"}

        with self.assertRaises(HunterClientDataError):
            parse_verify_email_data(test_data)
