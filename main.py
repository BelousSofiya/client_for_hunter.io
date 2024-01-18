"""Main file to get data."""

from data_storage import ClientDataStore
from hunter_client.endpoints import EndpointFactory

factory = EndpointFactory('e93c41dd45281f55bbb854ec1e86719c50b90d5d')
domain_search = factory.get_endpoint('domain-search')
email_finder = factory.get_endpoint('email-finder')
email_verifier = factory.get_endpoint('email-verifier')

data_storage = ClientDataStore()

# to get data from hunter.io

emails_by_domain = domain_search.execute('GET', 'stripe.com')
email_by_domain_first_last_name = email_finder.execute('GET', 'reddit.com', 'Alexis', 'Ohanian')
email_verified = email_verifier.execute('GET', 'patrik@stripe.com')

# to add data to storage and update data

data_storage.add_emails(emails_by_domain)
data_storage.add_emails(email_by_domain_first_last_name)
data_storage.update_email('patrik@stripe.com', email_verified)
