#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import random
import sys
import time

import requests

_sleep = [2 ** i / 32. for i in range(8)]


def http_get(url):
    print('GET', url, file=sys.stderr)
    time.sleep(random.choice(_sleep))
    ua = str(
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/39.0.2171.96 Safari/537.37'
    )
    headers = {'User-Agent': ua}
    return requests.get(url, headers=headers)


__all__ = [
    'http_get'
]
