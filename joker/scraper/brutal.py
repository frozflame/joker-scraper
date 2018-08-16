#!/usr/bin/env python3

import re

"""
Retrieve info from an HTML page using REGEX
"""


def attribute_reap(html, attrname, pattern=None):
    regex = re.compile(r'{}\s*=\s*"([^"]+)"'.format(attrname))
    for mat in regex.finditer(html):
        href = mat.groups()[-1]
        if pattern and re.search(pattern, href) is None:
            continue
        yield href


def href_reap(html, pattern=None):
    return attribute_reap(html, 'href', pattern=pattern)


def src_reap(html, pattern=None):
    return attribute_reap(html, 'src', pattern=pattern)


def url_parentheses_reap(html, pattern=None):
    regex = re.compile(r'url\(([^)]+)\)')
    for mat in regex.finditer(html):
        url = mat.groups()[-1]
        if pattern and re.search(pattern, url) is None:
            continue
        yield url


known_schemes = [
    'http', 'https', 'ftp', 'ed2k', 'magnet', 'freenet', 'thunder']


def url_scheme_reap(html, pattern=None):
    p1 = '|'.join(known_schemes)
    regex = re.compile(r'=\s*"((?:{}):[^"]+)"'.format(p1))
    for mat in regex.finditer(html):
        url = mat.groups()[-1]
        if pattern and re.search(pattern, url) is None:
            continue
        yield url


def brutal_link_reap(html, pattern):
    """results may repeat"""
    for link in attribute_reap(html, r'(src|href)', pattern=pattern):
        yield link
    for link in url_parentheses_reap(html, pattern=pattern):
        yield link
    for link in url_scheme_reap(html, pattern=pattern):
        yield link
