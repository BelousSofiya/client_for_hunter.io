# My solution of test task

## The task:

Choose any service and make a client for it, 2-3 endpoints will be enough + add a service that takes some values and 
saves the results, you can simply save it in a local variable.

As an example:
https://hunter.io/api-documentation/v2
Implement in the client sending a request to check and verify the email.
And add an email verification service + CRUD for the results, you can use a variable for the storage. Upload to github 
and package it.

Typing is required.
Use this linter: https://github.com/wemake-services/wemake-python-styleguide
setup.cfg https://gist.github.com/dfirst/0957711a40d640d335e128eec4c17f21

## To enjoy my solution:

### Install dependencies:

- pip install -r requirements.txt

### Check code by linter:

- python -m flake8

### Run tests:

- python -m unittest

### Check types:

- python -m mypy parsers.py main.py data_storage.py api_client.py exceptions.py

### Usage example:

- Create account on [hunter.io](https://hunter.io) and get API key

```
client = HunterHelper(<your API key>)

# to get data from hunter.io

email_by_domain_first_last_name = client.get_email_by_domain_first_last_name('reddit.com', 'Alexis', 'Ohanian')
emails_by_domain = client.get_emails_by_domain('stripe.com')
email_verified = client.verify_email('patrik@stripe.com')

# to check saved data

all data = client.get_all_data()
```
