"""API client for hunter.io."""

import requests


class HunterClient(object):
    """API client for hunter.io."""

    def __init__(self) -> None:
        """Init HunterClient with base url."""
        self.base_url = 'https://api.hunter.io/v2/'

    def get(self, path: str, params_for_url: dict, timeout: int = 30) -> dict:
        """Send get request to API endpoint.

        Send get request.
        Returns response body as dict.
        Rise exception if status is not OK or failed to decode body.
        """
        url = '{base_url}{path}'.format(base_url=self.base_url, path=path)
        response = requests.get(url, params=params_for_url, timeout=timeout)
        response.raise_for_status()
        return response.json()
