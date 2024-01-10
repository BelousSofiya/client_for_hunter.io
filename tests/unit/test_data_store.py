from unittest import TestCase
from uuid import uuid4

from data_storage import ClientDataStore


class AddEmailsTests(TestCase):

    def setUp(self):
        self.test_storage = ClientDataStore()
        self.id = str(uuid4())
        self.id2 = str(uuid4())

    def test_add_emails_to_empty_store(self):
        test_data = {'test_email_1': {'id': self.id, 'domains': ['test_domain_1']}}
        self.test_storage.add_emails(test_data)
        self.assertEqual(self.test_storage.own_data, test_data)

    def test_add_emails_to_store_with_data(self):

        self.test_storage.own_data = {'test_email_2': {'id': self.id2, 'domains': ['test_domain_2']}}
        test_data = {'test_email_1': {'id': self.id, 'domains': ['test_domain_1']}}
        result_data_in_storage = {'test_email_2': {'id': self.id2, 'domains': ['test_domain_2']},
                                  'test_email_1': {'id': self.id, 'domains': ['test_domain_1']}}
        self.test_storage.add_emails(test_data)
        self.assertEqual(self.test_storage.own_data, result_data_in_storage)

    def test_add_emails_to_store_where_this_email_already_exists(self):
        self.test_storage.own_data = {'test_email_1': {'id': self.id, 'domains': ['test_domain_1']}}
        test_data = {'test_email_1': {'id': self.id, 'domains': ['test_domain_1']}}
        self.test_storage.add_emails(test_data)
        self.assertEqual(self.test_storage.own_data, test_data)


class UpdateEmailTests(TestCase):
    def setUp(self):
        self.test_storage = ClientDataStore()
        self.id = str(uuid4())

    def test_update_existing_email(self):
        self.test_storage.own_data = {'test_email_1': {'id': self.id, 'domains': ['test_domain_1']}}
        self.test_storage.update_email('test_email_1', {'email_status': 'accept_all', 'email_result': 'risky'})
        result_data_in_storage = {'test_email_1': {'id': self.id, 'domains': ['test_domain_1'],
                                                   'email_status': 'accept_all', 'email_result': 'risky'}}
        self.assertEqual(self.test_storage.own_data, result_data_in_storage)

    def test_update_email_not_found(self):
        self.test_storage.own_data = {'test_email_1': {'id': self.id, 'domains': ['test_domain_1']}}
        self.test_storage.update_email('test_email_2', {'email_status': 'accept_all', 'email_result': 'risky'})
        result_data_in_storage = {'test_email_1': {'id': self.id, 'domains': ['test_domain_1'],
                                                   'email_status': 'accept_all', 'email_result': 'risky'}}
        self.assertNotEqual(self.test_storage.own_data, result_data_in_storage)
