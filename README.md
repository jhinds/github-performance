This is a simple program to get profile metrics from some of github's api.

There is a rate limit to the amount of requests you can send to github's api. To increase the rate limit pass in your github credentials by setting the environment variables ***GIT_USERNAME*** and ***GIT_PASSWORD***.

This program uses the library [requests](http://docs.python-requests.org/en/latest/).

The program takes in a commandline argument of `-n` if you would like to specify how many times to repeat the request.

You can run the program via the command line:

```python3 PerformanceProfiler.py -n 3```
