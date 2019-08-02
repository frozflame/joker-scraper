#!/usr/bin/env python3
# coding: utf-8

from __future__ import unicode_literals

import re

from joker.cast import regular_cast


def astext(soup):
    try:
        return soup.text
    except AttributeError:
        return


def _extract_numstr(soup):
    if soup is None:
        return
    s = astext(soup)
    try:
        return re.findall(r'[0-9,. ]+', s)[0]
    except IndexError:
        return


def asnum(soup):
    return regular_cast(_extract_numstr(soup), int, float, None)


def asint(soup):
    return regular_cast(_extract_numstr(soup), int, None)


def attribute_extract(soup, css_selector, attrname, pattern=None):
    for tag in soup.find_all(css_selector):
        val = tag.get(attrname, '')
        if pattern and re.search(pattern, val) is None:
            continue
        yield val
