#!/usr/bin/env python
print('If you get error "ImportError: No module named \'six\'" install six:\n'+\
    '$ sudo pip install six');
print('If you get error "ImportError: No module named \'eventlet\'" install' +\
    'eventlet:\n$ sudo pip install eventlet');
print('To enable your free eval account and get CUSTOMER, YOURZONE and ' + \
    'YOURPASS, please contact sales@brightdata.com')
import sys
import eventlet
if sys.version_info[0]==2:
    import six
    from six.moves.urllib import request
if sys.version_info[0]==3:
    from eventlet.green.urllib import request
import random
import socket

super_proxy = socket.gethostbyname('zproxy.lum-superproxy.io')

class SingleSessionRetriever:

    url = "http://%s-session-%s:%s@"+super_proxy+":%d"
    port = 22225

    def __init__(self, username, password, requests_limit, failures_limit):
        self._username = username
        self._password = password
        self._requests_limit = requests_limit
        self._failures_limit = failures_limit
        self._reset_session()

    def _reset_session(self):
        session_id = random.random()
        proxy = SingleSessionRetriever.url % (self._username, session_id, self._password,
                                              SingleSessionRetriever.port)
        proxy_handler = request.ProxyHandler({'http': proxy, 'https': proxy})
        self._opener = request.build_opener(proxy_handler)
        self._requests = 0
        self._failures = 0

    def retrieve(self, url, timeout):
        while True:
            if self._requests == self._requests_limit:
                self._reset_session()
            self._requests += 1
            try:
                timer = eventlet.Timeout(timeout)
                result = self._opener.open(url).read()
                timer.cancel()
                return result
            except:
                timer.cancel()
                self._failures += 1
                if self._failures == self._failures_limit:
                    self._reset_session()


class MultiSessionRetriever:

    def __init__(self, username, password, session_requests_limit, session_failures_limit):
        self._username = username
        self._password = password
        self._sessions_stack = []
        self._session_requests_limit = session_requests_limit
        self._session_failures_limit = session_failures_limit

    def retrieve(self, urls, timeout, parallel_sessions_limit, callback):
        pool = eventlet.GreenPool(parallel_sessions_limit)
        for url, body in pool.imap(lambda url: self._retrieve_single(url, timeout), urls):
            callback(url, body)

    def _retrieve_single(self, url, timeout):
        if self._sessions_stack:
            session = self._sessions_stack.pop()
        else:
            session = SingleSessionRetriever(self._username, self._password,
                                             self._session_requests_limit, self._session_failures_limit)
        body = session.retrieve(url, timeout)
        self._sessions_stack.append(session)
        return url, body

def output(url, body):
    print(body)

n_total_req = 100
req_timeout = 10
n_parallel_exit_nodes = 10
switch_ip_every_n_req = 10
max_failures = 2

MultiSessionRetriever('[REDACTED]', '[REDACTED]', switch_ip_every_n_req, max_failures).retrieve(
    ["http://lumtest.com/myip.json"] * n_total_req, req_timeout, n_parallel_exit_nodes, output)
