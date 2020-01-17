#!/usr/bin/env python3
# coding: utf-8

import gzip
import hashlib
import logging
import os
import traceback

logger = logging.getLogger(__name__)


class DiskCache(object):
    def __init__(self, dirpath):
        if not os.path.isdir(dirpath):
            raise ValueError('not a dir: ' + dirpath)
        self.dirpath = dirpath

    def get_path(self, key):
        return os.path.join(self.dirpath, key)

    def load(self, key):
        path = self.get_path(key)
        if not os.path.exists(path):
            return
        logger.debug('use cached: ' + path)
        try:
            content = gzip.open(path).read()
            hb = content[-16:]
            content = content[:-16]
            if hashlib.md5(content).digest() == hb:
                return content
            logger.debug('md5 hash mismatch')
        except IOError:
            traceback.print_exc()

    def save(self, key, content):
        path = self.get_path(key)
        logger.debug('save to cache: ' + path)
        hb = hashlib.md5(content).digest()
        with gzip.open(path, 'wb') as fout:
            fout.write(content)
            fout.write(hb)
        return content


class ScatteredDiskCache(DiskCache):
    def __init__(self, dirpath, prefixlen=4):
        DiskCache.__init__(self, dirpath)
        self.prefixlen = prefixlen

    def get_path(self, key):
        prefix = key[:self.prefixlen]
        pdirpath = os.path.join(self.dirpath, prefix)
        if not os.path.isdir(pdirpath):
            os.makedirs(pdirpath, exist_ok=True)
        return os.path.join(pdirpath, key)


SimpleDiskCache = DiskCache
