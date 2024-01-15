"""API client for hunter.io."""

import requests
from requests.exceptions import HTTPError, JSONDecodeError

from hunter_helper.exceptions import HunterClientDataError, HunterClientHTTPError


class HunterClient(object):
    """API client for hunter.io."""

    def __init__(self) -> None:
        """Init HunterClient with base url."""
        self.base_url = 'https://api.hunter.io/v2/'

    def get(self, path: str, params_for_url: dict, timeout: int = 30) -> dict:
        """Send get request to API endpoint.

        Send get request.
        Returns response body as dict.
        rise exception if status is not OK or failed to decode body.
        """
        try:
            return self._get_response(path, params_for_url, timeout)
        except HTTPError as error:
            raise HunterClientHTTPError(status=error.response.status_code, message=error.response.text)
        except JSONDecodeError:
            raise HunterClientDataError('Failed to decode hunter.io response')

    def _get_response(self, path: str, params_for_url: dict, timeout: int) -> dict:
        url = '{base_url}{path}'.format(base_url=self.base_url, path=path)
        response = requests.get(url, params=params_for_url, timeout=timeout)
        response.raise_for_status()
        return response.json()
