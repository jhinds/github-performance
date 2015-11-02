__author__ = 'jonathanhinds'
import requests
import statistics
import argparse


class PerformanceProfiler():

    def sort_key_performance(self):
        sort_metrics = []
        sort_metrics.append(self.run_suite(self,  self.search, sort='star', order='asc'))
        sort_metrics.append(self.run_suite(self, self.search, sort='star', order='desc'))
        sort_metrics.append(self.run_suite(self, self.search, sort='forks', order='asc'))
        sort_metrics.append(self.run_suite(self, self.search, sort='forks', order='desc'))
        sort_metrics.append(self.run_suite(self, self.search, sort='updated', order='asc'))
        sort_metrics.append(self.run_suite(self, self.search, sort='updated', order='desc'))
        sort_metrics.sort()


    def profile_pages(self):
        pass

    def get_django_repo(self, ref):
        headers = {'Accept': 'application/vnd.github.v3+json'}
        url = 'https://api.github.com/repos/django/django/contents/js_tests/gis/mapwidget.test.js'
        params = {'ref': ref}
        response = requests.get(url=url, headers=headers, params=params)
        return response

    def find_angular_repos(self):
        return self.search(self, q='angular')

    def find_angular_coffee_script_repos(self):
        return self.search(q=['angular', {'language': 'coffeescript'}])

    def search(self,
               sort=None,
               order=None,
               q=None):
        url = 'https://api.github.com'
        params = {'q': q,
                  'sort': sort,
                  'order': order}
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.get(url=url, headers=headers, params=params)
        return response

    def print_metrics(self, api, mean, std_dv, failures=0):
        if failures:
            print('API: %s \n\nMEAN REQ TIME: %d\n\nALL SUCCESS: false\n\nNUM FAILURES: %s\n\nSTD DEV: %d\n\n' % (api, mean, failures, std_dv))
        else:
            print('API: %s \n\nMEAN REQ TIME: %d\n\nALL SUCCESS: true\n\nSTD DEV: %d\n\n' % (api, mean, std_dv))

    def run_suite(self, method, **kwargs):
        request_time_list = []
        failures = 0
        for i in range(0, n):
            response = method(self, kwargs)
            # response = requests.get('https://www.google.com')
            request_time_list.append(response.elapsed.microseconds/1000)
            if response.status_code is not 200:
                failures += 1
        mean = statistics.mean(request_time_list)
        pstd_dv = statistics.pstdev(request_time_list)
        self.print_metrics(self, 'get angular', mean, pstd_dv, failures)
        return mean, pstd_dv

    def run_all(self):
        self.run_suite(self, self.find_angular_repos)
        self.run_suite(self, self.find_angular_coffee_script_repos)
        self.run_suite(self, self.find_angular_coffee_script_repos)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='add in a number of requests')
    parser.add_argument('-n', action='store', type=int, help='number of times to process the request', default=1)
    args = parser.parse_args()
    n = args.n
    profile = PerformanceProfiler
    profile.run_all(profile)
