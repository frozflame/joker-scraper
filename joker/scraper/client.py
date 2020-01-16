#!/usr/bin/env python3
# coding: utf-8

import requests


default_useragent = (
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) '
    'Gecko/20100101 Firefox/64.0'
)


class Client(object):
    def __init__(self):
        self.sess = requests.session()
        self.sess.headers['User-Agent'] = default_useragent

    def get_pages(self, urls):
        headers = {}
        for url in urls:
            if not url:
                self.sess.headers.pop('Referer', 0)
                continue
            resp = self.sess.get(url, headers=headers)
            self.sess.headers['Referer'] = url
            print(self.sess.headers)
            yield resp

