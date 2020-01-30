#!/usr/bin/env python3
# coding: utf-8

import time
import logging
import math

logger = logging.getLogger(__name__)


class RandomPause(object):
    def __init__(self, seconds):
        self.seconds = list(seconds) or [0]
        self.enabled = True

    def __call__(self):
        ix = int(time.time() * 1024) % len(self.seconds)
        tsec = self.seconds[ix]
        logger.debug('RandomPause -- pausing for %s seccond(s)', tsec)
        if self.enabled:
            time.sleep(tsec)
        return tsec

    @classmethod
    def simple(cls, func, *pargs_for_range):
        return cls(func(x) for x in range(*pargs_for_range))

    @classmethod
    def preset_invfac(cls, *pargs_for_range):
        return cls.simple(lambda x: 1. / math.factorial(x), *pargs_for_range)

    @classmethod
    def preset_expon(cls, *pargs_for_range):
        return cls.simple(lambda x: 2 ** x, *pargs_for_range)
