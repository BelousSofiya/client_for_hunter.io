from unittest import TestCase
from unittest.mock import patch

from hunter_client.endpoints import EndpointFactory


class FunctionalTestsHelper(TestCase):

    def setUp(self):
        client_patcher = patch('hunter_client.endpoints.HunterClient')
        self.mock_client_get = client_patcher.start().return_value.send_request
        self.addCleanup(client_patcher.stop)

        uuid_patcher = patch('hunter_client.parsers.uuid4')
        mock_uuid = uuid_patcher.start()
        mock_uuid.side_effect = [
            'f26d75e4-3bb7-41c0-8e87-87aea01bd953',
            '5606bdab-ab9d-4354-a974-fbe870a54101',
        ]

        test_api_key = 'test_api_key'
        self.factory = EndpointFactory(test_api_key)
        self.domain_search = self.factory.get_endpoint('domain-search')
        self.email_finder = self.factory.get_endpoint('email-finder')
        self.email_verifier = self.factory.get_endpoint('email-verifier')


class EmailsByDomainTests(FunctionalTestsHelper):

    def test_get_emails_by_domain(self):
        test_domain = 'test_domain'

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
        expected = {
            'test_email_1': {
                'id': 'f26d75e4-3bb7-41c0-8e87-87aea01bd953',
                'domains': ['test_domain_1', 'test_domain_2']
            },
            'test_email_2': {
                'id': '5606bdab-ab9d-4354-a974-fbe870a54101',
                'domains': ['test_domain_3']
            }
        }
        actual = self.domain_search.execute('GET', test_domain)

        self.assertEqual(expected, actual)


class EmailByDomainFirstLastNameTests(FunctionalTestsHelper):

    def test_get_email_by_domain_first_last_name(self):
        test_domain = 'test_domain'
        test_first_name = 'first'
        test_last_name = 'last'
        test_email = 'test_email_3'

        self.mock_client_get.return_value = {
            'data': {
                'email': test_email,
                'sources': [{'domain': 'test_domain_3'}]
            }
        }
        expected = {'test_email_3': {
            'id': 'f26d75e4-3bb7-41c0-8e87-87aea01bd953',
            'domains': ['test_domain_3']
            }
        }
        actual = self.email_finder.execute('GET', test_domain, test_first_name, test_last_name)

        self.assertEqual(expected, actual)


class VerificationEmailTests(FunctionalTestsHelper):

    def test_verify_email(self):
        test_email = 'test_email_3'

        self.mock_client_get.return_value = {
            'data': {'email': test_email, 'status': 'good', 'result': 'positive)'}
        }

        expected = {test_email: {'email_status': 'good', 'email_result': 'positive)'}}
        actual = self.email_verifier.execute('GET', test_email)
        self.assertEqual(expected, actual)


class NotImplementedEndpointTests(FunctionalTestsHelper):

    def test_not_implemented_endpoint(self):
        with self.assertRaises(NotImplementedError):
            self.factory.get_endpoint('not-implemented')
