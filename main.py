"""Main file to get data."""

from data_storage import ClientDataStore
from hunter_helper.hunter_helper import EmailByDomainFirstLastName, EmailsByDomain, EmailVerification

if __name__ == '__main__':
    endpoint1 = EmailsByDomain(<your API key>)
    endpoint2 = EmailByDomainFirstLastName(<your API key>)
    endpoint3 = EmailVerification(<your API key>)
    data_storage = ClientDataStore()

# to get data from hunter.io

    emails_by_domain = endpoint1.execute('stripe.com')
    email_by_domain_first_last_name = endpoint2.execute('reddit.com', 'Alexis', 'Ohanian')
    email_verified = endpoint3.execute('patrik@stripe.com')

# to add data to storage and update data

    data_storage.add_emails(emails_by_domain)
    data_storage.add_emails(email_by_domain_first_last_name)
    data_storage.update_email('patrik@stripe.com', email_verified)
