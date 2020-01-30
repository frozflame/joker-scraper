#!/usr/bin/env python3
# coding: utf-8

import logging
import time
import requests

logger = logging.getLogger(__name__)

useragents = (
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:64.0) '
    'Gecko/20100101 Firefox/64.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.37 '
    '(KHTML, like Gecko) Chrome/39.0.2171.88 Safari/537.37',
)


def get_useragent():
    i = int(time.time()) % len(useragents)
    return useragents[i]


class DummyCache(object):
    def load(self, key):
        pass

    def save(self, key, content):
        pass


class _CacheWrapper(object):
    """Bypass cache when key is None"""

    def __init__(self, cache):
        self._cache = cache

    def load(self, key):
        if key is not None:
            return self._cache.load(key)

    def save(self, key, content):
        if key is not None:
            return self._cache.save(key, content)


class CachedResponse(object):
    __slots__ = ['content', 'url']
    status_code = 0
    reason = 'Cached'

    def __init__(self, content, url):
        self.content = content
        self.url = url

    @property
    def text(self):
        import chardet
        encoding = chardet.detect(self.content)['encoding']
        return self.content.decode(encoding)


class Client(object):
    def __init__(self, cache):
        self.sess = requests.Session()
        self.sess.headers['User-Agent'] = get_useragent()
        self.cache = _CacheWrapper(cache)

    @classmethod
    def cacheless(cls):
        return cls(DummyCache())

    @staticmethod
    def keygen(url, **kwargs):
        method = kwargs.get('method', 'get')
        if method.lower() == 'get':
            return url

    @staticmethod
    def pause(maxsec):
        if maxsec <= 0:
            return
        time.sleep(time.time() % maxsec)

    def request(self, url, **kwargs):
        if not url:
            self.sess.headers.pop('Referer', 0)
            return
        key = self.keygen(url, **kwargs)
        content = self.cache.load(key)
        if content is None:
            logger.debug('cache miss: %s', url)
            kwargs.setdefault('method', 'get')
            resp = self.sess.request(url=url, **kwargs)
            self.cache.save(key, resp.content)
            return resp
        self.sess.headers['Referer'] = url
        return CachedResponse(content, url)

    def post(self, url, **kwargs):
        kwargs.setdefault('method', 'post')
        return self.request(url, **kwargs)

    def get(self, url):
        return self.request(url)

    def batch_get(self, targets):
        for tar in targets:
            if isinstance(tar, (int, float)):
                yield self.pause(tar)
            yield self.get(tar)
