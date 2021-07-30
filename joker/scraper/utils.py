#!/usr/bin/env python3
# coding: utf-8

import time


def until_success(func, retry, sleep, *args, **kwargs):
    for ix in reversed(range(retry + 1)):
        try:
            return func(*args, **kwargs)
        except Exception:
            time.sleep(sleep)
            if ix == 0:
                raise


