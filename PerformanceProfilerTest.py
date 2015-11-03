
__author__ = 'jonathanhinds'
import unittest
from unittest.mock import patch
import requests
import responses
import PerformanceProfiler
class PerformanceProfilerTest(unittest.TestCase):


    @patch('requests.get')
    @patch('PerformanceProfiler.PerformanceProfiler')
    def check_git_creds(self, mock_profile, mock_request):
        mock_profile.search('sort', 'order')
        requests.get.assert_called_once_with('sort', 'order')


    @responses.activate
    def test_check_git_creds_fail(self):
        responses.add(responses.GET, 'https://api.github.com',
                      status=401,
                      content_type='application/json')
        response = requests.get('https://api.github.com', auth=('a','b'))
        assert response.status_code is 401

    @responses.activate
    def test_check_git_creds(self):
        responses.add(responses.GET, 'https://api.github.com',
                      status=200,
                      content_type='application/json')
        response = requests.get('https://api.github.com', auth=('correct','b'))
        assert response.status_code is 200

    def test_print_metrics(self):
        s = PerformanceProfiler.PerformanceProfiler.print_metrics(None, 'test', 1, 0, 0)
        print(s)
        assert 'test' in s
        assert '1 ms' in s
        assert 'true' in s
        assert 'FAILURES' not in s

    def test_print_metrics_w_failures(self):
        s = PerformanceProfiler.PerformanceProfiler.print_metrics(None, 'test', 1, 0, 1)
        print(s)
        assert 'test' in s
        assert '1 ms' in s
        assert 'false' in s
        assert 'FAILURES' in s

    @responses.activate
    def test_run_suite(self):
        responses.add(responses.GET, 'https://api.github.com',
                      status=200,
                      content_type='application/json',
                      body='{\'elapsed\': {\'microseconds\': 200}}')
        def mock():
            return requests.get('https://api.github.com')
        profile = PerformanceProfiler.PerformanceProfiler
        profile.n = 1
        # d = timedelta(microseconds=-1)
        m, sd, f = profile.run_suite(profile, mock)
        assert m is not 0
        assert f is 0
        assert sd == 0


    @responses.activate
    def test_run_suite_w_loops(self):
        responses.add(responses.GET, 'https://api.github.com',
                      status=200,
                      content_type='application/json',
                      body='{\'elapsed\': {\'microseconds\': 200}}')
        def mock():
            return requests.get('https://api.github.com')
        profile = PerformanceProfiler.PerformanceProfiler
        profile.n = 5
        m, sd, f = profile.run_suite(profile, mock)
        assert sd > 0


if __name__ == '__main__':
    unittest.main()