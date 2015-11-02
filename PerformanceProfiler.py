__author__ = 'jonathanhinds'
import requests
import statistics
import argparse
from operator import itemgetter
import os

class PerformanceProfiler():

    def __init__(self):
        git_username = os.getenv('GIT_USERNAME')
        git_password = os.getenv('GIT_PASSWORD')
        self.auth = (git_username, git_password)
        self.headers = {'Accept': 'application/vnd.github.v3+json'}

    def search(self,
               sort=None,
               order=None,
               q=None,
               page=None):
        url = 'https://api.github.com/search/repositories'
        params = {'q': q,
                  'sort': sort,
                  'order': order,
                  'page': page}
        response = requests.get(url=url, headers=self.headers, params=params, auth=self.auth)
        return response

    def sort_key_performance(self):
        print('###### Suite 2: Sort Key Performance ######\n')
        sorted_metrics = {}
        sorted_metrics.update({'star_asc': (self.run_suite(self.search, sort='star', order='asc'))})
        sorted_metrics.update({'star_desc': self.run_suite(self.search, sort='star', order='desc')})
        sorted_metrics.update({'forks_asc': self.run_suite(self.search, sort='forks', order='asc')})
        sorted_metrics.update({'forks_desc': self.run_suite(self.search, sort='forks', order='desc')})
        sorted_metrics.update({'updated_asc': self.run_suite(self.search, sort='updated', order='asc')})
        sorted_metrics.update({'updated_desc': self.run_suite(self.search, sort='updated', order='desc')})
        fastest = min(sorted_metrics, key=sorted_metrics.get)
        list_metrics = sorted(sorted_metrics.items(), key=itemgetter(1), reverse=True)
        for result in list_metrics:
            self.print_metrics([result[0]][0], [result[1]][0][0], [result[1]][0][1], [result[1]][0][2])
        self.get_page_profiles(fastest)

    def check_git_creds(self):
        response = requests.get('https://api.github.com', auth=self.auth)
        response.raise_for_status()

    def get_page_profiles(self, fastest):
        print('###### Suite 3: Page Performance ######\n')
        sort, order = fastest.split('_')
        params = {'sort': sort,
                  'order': order}
        first_page_response = self.search(sort=sort, order=order, q='angular')
        second_page_response = requests.get(first_page_response.links['next']['url'])
        last_page_response = requests.get(first_page_response.links['last']['url'])
        second_last_page_response = requests.get(last_page_response.links['prev']['url'],  auth=self.auth)

        mean, std_dv, failures = self.run_suite(self.search, sort=sort, order=order)
        self.print_metrics(fastest + ' page 1', mean, std_dv)
        mean, std_dv, failures = self.run_suite(requests.get, url=first_page_response.links['next']['url'], params=params, auth=self.auth)
        self.print_metrics(fastest + ' page 2', mean, std_dv)
        mean, std_dv, failures = self.run_suite(requests.get, url=second_page_response.links['next']['url'], params=params,  auth=self.auth)
        self.print_metrics(fastest + ' page 3', mean, std_dv)
        mean, std_dv, failures = self.run_suite(requests.get, url=first_page_response.links['last']['url'], params=params,  auth=self.auth)
        self.print_metrics(fastest + ' last page', mean, std_dv)
        mean, std_dv, failures = self.run_suite(requests.get, url=last_page_response.links['prev']['url'], params=params,  auth=self.auth)
        self.print_metrics(fastest + ' second to last page', mean, std_dv)
        mean, std_dv, failures = self.run_suite(requests.get, url=second_last_page_response.links['prev']['url'], params=params,  auth=self.auth)
        self.print_metrics(fastest + ' third to last page', mean, std_dv)

    def get_django_repo(self, ref):
        url = 'https://api.github.com/repos/django/django/contents/js_tests/gis/mapwidget.test.js'
        params = {'ref': ref}
        response = requests.get(url=url, headers=self.headers, params=params, auth=self.auth)
        return response

    def print_metrics(self, api, mean, std_dv, failures=0):
        if failures:
            print('API: %s \n\nMEAN REQ TIME: %d ms\n\nALL SUCCESS: false\n\nNUM FAILURES: %s\n\nSTD DEV: %d ms\n\n' % (api, mean, failures, std_dv))
        else:
            print('API: %s \n\nMEAN REQ TIME: %d ms\n\nALL SUCCESS: true\n\nSTD DEV: %d ms\n\n' % (api, mean, std_dv))

    def run_suite(self, method, **kwargs):
        request_time_list = []
        failures = 0
        for i in range(0, n):
            response = method(**kwargs)
            request_time_list.append(response.elapsed.microseconds/1000)
            if response.status_code is not 200:
                failures += 1
        mean = statistics.mean(request_time_list)
        pstd_dv = statistics.pstdev(request_time_list)
        return mean, pstd_dv, failures

    def run_all(self):
        self.check_git_creds()
        print('###### Suite 1: Angular ######\n')
        mean, pstd_dv, failures = self.run_suite(self.search, q='angular')
        self.print_metrics('Find Angular Repos', mean, pstd_dv, failures)
        mean, pstd_dv, failures = self.run_suite(self.search, q=['angular', {'language': 'coffeescript'}])
        self.print_metrics('Find Angular Repos with CoffeeScript', mean, pstd_dv, failures)
        self.sort_key_performance()
        mean, pstd_dv, failures = self.run_suite(self.get_django_repo, ref='master' )
        print('###### Suite 4: Django ######\n')
        self.print_metrics('Get mapwidget.test.js from Django master branch', mean, pstd_dv, failures)
        mean, pstd_dv, failures = self.run_suite(self.get_django_repo, ref='1.8.5')
        self.print_metrics('Get mapwidget.test.js from Django 1.8.5 tag', mean, pstd_dv, failures)

def main():
    profile = PerformanceProfiler()
    profile.run_all()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='add in a number of requests')
    parser.add_argument('-n', action='store', type=int, help='number of times to process the request', default=1)
    args = parser.parse_args()
    n = args.n
    main()

