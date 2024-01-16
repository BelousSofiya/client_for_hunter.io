from unittest import TestCase
from unittest.mock import patch

from hunter_helper.hunter_helper import HunterHelper, EmailsByDomain, EmailByDomainFirstLastName, EmailVerification


class FunctionalTestsHelper(TestCase):

    def setUp(self):
        client_patcher = patch('hunter_helper.hunter_helper.HunterClient')
        self.mock_client_get = client_patcher.start().return_value.get
        self.addCleanup(client_patcher.stop)

        uuid_patcher = patch('hunter_helper.parsers.uuid4')
        mock_uuid = uuid_patcher.start()
        mock_uuid.side_effect = [
            'f26d75e4-3bb7-41c0-8e87-87aea01bd953',
            '5606bdab-ab9d-4354-a974-fbe870a54101',
            # '3d66b9cf-16c8-446d-bffb-a327e0b7748a',
        ]

        test_api_key = 'test_api_key'
        self.subject = HunterHelper(test_api_key)
        self.subject1 = EmailsByDomain(test_api_key)
        self.subject2 = EmailByDomainFirstLastName(test_api_key)
        self.subject3 = EmailVerification(test_api_key)


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
        self.assertEqual(
            {'test_email_1': {'id': 'f26d75e4-3bb7-41c0-8e87-87aea01bd953',
                              'domains': ['test_domain_1', 'test_domain_2']},
             'test_email_2': {'id': '5606bdab-ab9d-4354-a974-fbe870a54101', 'domains': [
                 'test_domain_3']}}
            ,
            self.subject1.execute(test_domain)
        )


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

        self.assertEqual(
            {'test_email_3': {'id': 'f26d75e4-3bb7-41c0-8e87-87aea01bd953', 'domains': ['test_domain_3']}},
            self.subject2.execute(test_domain, test_first_name, test_last_name)
        )


class VerificationEmailTests(FunctionalTestsHelper):

    def test_verify_email(self):
        test_email = 'test_email_3'

        self.mock_client_get.return_value = {
            'data': {'email': test_email, 'status': 'good', 'result': 'positive)'}
        }
        self.assertEqual(
            {test_email: {'email_status': 'good', 'email_result': 'positive)'}},
            self.subject3.execute(test_email)
        )
