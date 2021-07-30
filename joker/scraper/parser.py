#!/usr/bin/env python3
# coding: utf-8

import re

from bs4 import BeautifulSoup
from bs4.element import Tag, Comment
from joker.cast import regular_cast


def astext(soup: Tag):
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


def remove_scripts(tag: Tag):
    for el in tag.select('script'):
        el.decompose()


def remove_comments(tag: Tag):
    for el in tag.find_all(string=lambda t: isinstance(t, Comment)):
        el.extract()


class ExtendedSoup(BeautifulSoup):
    def __init__(self, markup: str, features='lxml', *args, **kwargs):
        super().__init__(markup, features, *args, **kwargs)

    def insert_before(self, *args):
        pass

    def insert_after(self, *args):
        pass

    remove_scripts = remove_scripts
    remove_comments = remove_comments

    def save_html(self, path: str):
        with open(path, 'w') as fout:
            fout.write(str(self))
