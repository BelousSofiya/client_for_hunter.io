from unittest import TestCase
from unittest.mock import Mock, patch

from requests.exceptions import HTTPError, JSONDecodeError

from hunter_client.hunter_api_client import HunterClient


class GetTests(TestCase):

    def setUp(self):
        request_patcher = patch('hunter_client.hunter_api_client.requests')
        self.mock_request = request_patcher.start()
        self.mock_response = Mock()
        self.mock_request.request.return_value = self.mock_response
        self.addCleanup(request_patcher.stop)

        self.subject = HunterClient()

        self.test_path = 'test_path'
        self.test_props = {'test': 'props'}

    def test_success(self):
        test_response_payload = {'test': 'data'}
        self.mock_response.json.return_value = test_response_payload

        actual = self.subject.send_request('GET', self.test_path, self.test_props)
        self.assertEqual(test_response_payload, actual)

    def test_status_not_ok_rises_exception(self):
        resp = Mock()
        resp.status_code = 500
        resp.text = 'Ops!'

        self.mock_response.raise_for_status.side_effect = HTTPError(response=resp)

        with self.assertRaises(HTTPError):
            self.subject.send_request('GET', self.test_path, self.test_props)

    def test_not_json_response_body_rises_exception(self):
        self.mock_response.return_value = '<h1>Hello world<h1>'
        self.mock_response.raise_for_status.side_effect = JSONDecodeError('Opps!', 'doc', 0)

        with self.assertRaises(JSONDecodeError):
            self.subject.send_request('GET', self.test_path, self.test_props)
