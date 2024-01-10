from unittest import TestCase
from unittest.mock import Mock, patch

from requests.exceptions import HTTPError, JSONDecodeError

from api_client import HunterClient
from exceptions import HunterClientDataError, HunterClientHTTPError


class GetTests(TestCase):

    def setUp(self):
        request_patcher = patch('api_client.requests')
        self.mock_request = request_patcher.start()
        self.mock_response = Mock()
        self.mock_request.get.return_value = self.mock_response
        self.addCleanup(request_patcher.stop)

        self.subject = HunterClient()

        self.test_path = 'test_path'
        self.test_props = {'test': 'props'}

    def test_success(self):
        test_response_payload = {'test': 'data'}
        self.mock_response.json.return_value = test_response_payload

        actual = self.subject.get(self.test_path, self.test_props)

        self.assertEqual(test_response_payload, actual)

    def test_status_not_ok_rises_exception(self):
        resp = Mock()
        resp.status_code = 500
        resp.text = 'Ops!'

        self.mock_response.raise_for_status.side_effect = HTTPError(response=resp)

        with self.assertRaises(HunterClientHTTPError):
            self.subject.get(self.test_path, self.test_props)

    def test_not_json_response_body_rises_exception(self):
        test_response_payload = '<h1>Hello world<h1>'
        self.mock_response.return_value = test_response_payload
        self.mock_response.raise_for_status.side_effect = JSONDecodeError('Opps!', 'doc', 0)

        with self.assertRaises(HunterClientDataError):
            self.subject.get(self.test_path, self.test_props)
