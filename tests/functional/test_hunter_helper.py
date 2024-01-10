from unittest import TestCase
from unittest.mock import patch

from main import HunterHelper


class HunterHelperFlowTests(TestCase):

    def setUp(self):
        client_patcher = patch('main.HunterClient')
        self.mock_client_get = client_patcher.start().return_value.get
        self.addCleanup(client_patcher.stop)

        uuid_patcher = patch('parsers.uuid4')
        mock_uuid = uuid_patcher.start()
        mock_uuid.side_effect = [
            'f26d75e4-3bb7-41c0-8e87-87aea01bd953',
            '5606bdab-ab9d-4354-a974-fbe870a54101',
            '3d66b9cf-16c8-446d-bffb-a327e0b7748a',
        ]

        test_api_key = 'test_api_key'
        self.subject = HunterHelper(test_api_key)

    def test_email_investigation_flow(self):
        test_domain = 'test_domain'
        test_first_name = 'first'
        test_last_name = 'last'
        test_email = 'test_email_3'

        # look for emails by domain
        self.mock_client_get.return_value = {
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
        self.assertEqual(
            ['test_email_1', 'test_email_2'],
            self.subject.get_emails_by_domain(test_domain)
        )
        # assert data store
        expected_data_in_store = {
            'test_email_1': {
                'id': 'f26d75e4-3bb7-41c0-8e87-87aea01bd953',
                'domains': ['test_domain_1', 'test_domain_2']
            },
            'test_email_2': {
                'id': '5606bdab-ab9d-4354-a974-fbe870a54101',
                'domains': ['test_domain_3']
            }
        }
        self.assertEqual(
            expected_data_in_store,
            self.subject.get_all_data()
        )

        # look for email by domain, first and last names
        self.mock_client_get.return_value = {
            'data': {
                'email': test_email,
                'sources': [{'domain': 'test_domain_3'}]
            }
        }
        self.assertEqual(
            test_email,
            self.subject.get_email_by_domain_first_last_name(test_domain, test_first_name, test_last_name)
        )
        # assert data store
        expected_data_in_store = {
            'test_email_1': {
                'id': 'f26d75e4-3bb7-41c0-8e87-87aea01bd953',
                'domains': ['test_domain_1', 'test_domain_2']
            },
            'test_email_2': {
                'id': '5606bdab-ab9d-4354-a974-fbe870a54101',
                'domains': ['test_domain_3']
            },
            'test_email_3': {
                'domains': ['test_domain_3'],
                'id': '3d66b9cf-16c8-446d-bffb-a327e0b7748a'
            }
        }
        self.assertEqual(
            expected_data_in_store,
            self.subject.get_all_data()
        )

        # verify email accessibility
        self.mock_client_get.return_value = {
            'data': {'status': 'good', 'result': 'positive)'}
        }
        self.assertEqual(
            {'email_status': 'good', 'email_result': 'positive)'},
            self.subject.verify_email(test_email)
        )
        # assert data store
        expected_data_in_store = {
            'test_email_1': {
                'id': 'f26d75e4-3bb7-41c0-8e87-87aea01bd953',
                'domains': ['test_domain_1', 'test_domain_2']
            },
            'test_email_2': {
                'id': '5606bdab-ab9d-4354-a974-fbe870a54101',
                'domains': ['test_domain_3']
            },
            'test_email_3': {
                'domains': ['test_domain_3'],
                'id': '3d66b9cf-16c8-446d-bffb-a327e0b7748a',
                'email_result': 'positive)',
                'email_status': 'good',
            }
        }
        self.assertEqual(
            expected_data_in_store,
            self.subject.get_all_data()
        )
