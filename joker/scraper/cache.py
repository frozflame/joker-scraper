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

    def load(self, key):
        path = os.path.join(self.dirpath, key)
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
        path = os.path.join(self.dirpath, key)
        hb = hashlib.md5(content).digest()
        with gzip.open(path, 'wb') as fout:
            fout.write(content)
            fout.write(hb)
        return content


SimpleDiskCache = DiskCache
