"""Main file to get data."""

from data_storage import ClientDataStore
from hunter_helper.hunter_helper import HunterHelper

if __name__ == '__main__':
    client = HunterHelper(<your API key>)
    data_storage = ClientDataStore()
# to get data from hunter.io

    email_by_domain_first_last_name = client.get_email_by_domain_first_last_name('reddit.com', 'Alexis', 'Ohanian')
    emails_by_domain = client.get_emails_by_domain('stripe.com')
    email_verified = client.verify_email('patrik@stripe.com')

# to add data to storage and update data

    data_storage.add_emails(emails_by_domain)
    data_storage.add_emails(email_by_domain_first_last_name)
    data_storage.update_email('patrik@stripe.com', email_verified)
