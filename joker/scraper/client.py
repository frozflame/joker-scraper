#!/usr/bin/env python3
# coding: utf-8

import requests


default_useragent = (
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) '
    'Gecko/20100101 Firefox/64.0'
)


class DummyCache(object):
    def load(self, key):
        pass

    def save(self, key, content):
        pass


class Client(object):
    def __init__(self, cache):
        self.sess = requests.Session()
        self.sess.headers['User-Agent'] = default_useragent
        self.cache = cache

    @classmethod
    def cacheless(cls):
        return cls(DummyCache())

    @classmethod
    def keygen(cls, url):
        return url

    def get_pages(self, urls):
        headers = {}
        for url in urls:
            if not url:
                self.sess.headers.pop('Referer', 0)
                continue
            key = self.keygen(url)
            content = self.cache.load(key)
            if content is None:
                content = self.sess.get(url, headers=headers).content
                self.cache.save(key, content)
            self.sess.headers['Referer'] = url
            yield content

