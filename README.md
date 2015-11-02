This is a simple program to get profile metrics of some of githubs api.

To get increase the rate limit for the github api you can pass in your github credentials by setting environment variables 'GIT_USERNAME' and 'GIT_PASSWORD'.

This program takes has two dependencies, [requests](http://docs.python-requests.org/en/latest/) and [responses](https://github.com/getsentry/responses)

The program takes in a commandline argument of -n to determine how many requests should the program make.

You can run the program via the command line:
`python3 PerformanceProfiler.py -n 3`