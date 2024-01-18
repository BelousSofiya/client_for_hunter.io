"""API client for hunter.io."""

import requests


class HunterClient(object):
    """API client for hunter.io."""

    def __init__(self) -> None:
        """Init HunterClient with base url."""
        self.base_url = 'https://api.hunter.io/v2/'

    def send_request(self, method: str, path: str, params_for_url: dict, timeout: int = 30) -> dict:
        """Send request to API endpoint. Returns response body as dict."""
        if method != 'GET':
            raise NotImplementedError('Only GET method allowed')

        url = '{base_url}{path}'.format(base_url=self.base_url, path=path)
        response = requests.request(method, url, params=params_for_url, timeout=timeout)
        response.raise_for_status()
        return response.json()
