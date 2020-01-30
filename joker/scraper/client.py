#!/usr/bin/env python3
# coding: utf-8

import logging
import time

from joker.diskcache.http import HTTPClient

logger = logging.getLogger(__name__)


class Client(HTTPClient):
    useragents = (
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) '
        'Gecko/20100101 Firefox/64.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.37 '
        '(KHTML, like Gecko) Chrome/39.0.2171.88 Safari/537.37',
    )

    def __init__(self, cache):
        HTTPClient.__init__(self, cache)
        self.sess.headers['User-Agent'] = self.get_useragent()

    @classmethod
    def get_useragent(cls):
        i = int(time.time()) % len(cls.useragents)
        return cls.useragents[i]
