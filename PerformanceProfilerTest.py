__author__ = 'jonathanhinds'
import unittest
import responses
from PerformanceProfiler import PerformanceProfiler

class PerformanceProfilerTest(unittest.TestCase):

    def __init__(self):
        self.profiler = PerformanceProfiler


    @responses.activate
    def test_get_angular(self):
        responses.add(responses.GET, 'https://api.github.com',
                      status = 200)
        r = PerformanceProfiler.find_angular_repos(self.profiler)
        assert r.status_code == 200

if __name__ == "__main__":
    unittest.main()